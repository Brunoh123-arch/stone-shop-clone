import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.error
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CATALOG_PATH = os.path.join(ROOT_DIR, 'config', 'products_video_catalog.json')
DEFAULT_REPORT_PATH = os.path.join(ROOT_DIR, 'data', 'sentinel_health_report.json')

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'

def probe_single_video(item, timeout=10, retries=2):
    url = item['catbox_url']
    req = urllib.request.Request(url, headers={
        'User-Agent': USER_AGENT,
        'Range': 'bytes=0-10'
    })

    last_error = None
    for attempt in range(retries + 1):
        t0 = time.perf_counter()
        try:
            resp = urllib.request.urlopen(req, timeout=timeout)
            try:
                latency = round((time.perf_counter() - t0) * 1000, 1)
                status = getattr(resp, 'status', getattr(resp, 'code', 200))
                headers = resp.headers if hasattr(resp, 'headers') else {}
                cr = headers.get('Content-Range', '') if hasattr(headers, 'get') else ''
                total_bytes = 0
                if cr:
                    m = re.search(r'/(\d+)', cr)
                    if m:
                        total_bytes = int(m.group(1))

                if status not in (200, 206):
                    state = 'DEAD'
                elif latency >= 1500:
                    state = 'SLOW'
                else:
                    state = 'HEALTHY'

                return {
                    **item,
                    "status_code": status,
                    "latency_ms": latency,
                    "total_bytes": total_bytes,
                    "total_mb": round(total_bytes / (1024 * 1024), 2) if total_bytes else 0,
                    "state": state,
                    "checked_at": datetime.now(timezone.utc).isoformat()
                }
            finally:
                if hasattr(resp, 'close'):
                    resp.close()
        except urllib.error.HTTPError as e:
            latency = round((time.perf_counter() - t0) * 1000, 1)
            return {
                **item,
                "status_code": e.code,
                "latency_ms": latency,
                "total_bytes": 0,
                "total_mb": 0,
                "state": 'DEAD',
                "error": str(e),
                "checked_at": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            last_error = str(e)
            time.sleep(0.5)

    latency = round((time.perf_counter() - t0) * 1000, 1)
    return {
        **item,
        "status_code": 0,
        "latency_ms": latency,
        "total_bytes": 0,
        "total_mb": 0,
        "state": 'DEAD',
        "error": last_error or "Timeout / Connection Error",
        "checked_at": datetime.now(timezone.utc).isoformat()
    }

def run_sentinel_scan(product_filter=None, max_threads=15, timeout=10, output_path=DEFAULT_REPORT_PATH):
    resolved_output = os.path.abspath(output_path) if not os.path.isabs(output_path) else output_path

    if not os.path.exists(CATALOG_PATH):
        raise FileNotFoundError(f"Catálogo {CATALOG_PATH} não encontrado. Execute generate_video_catalog.py primeiro.")

    with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
        cat = json.load(f)

    all_videos = cat.get('videos', [])
    if product_filter:
        videos = [v for v in all_videos if product_filter.lower() in v['namespace'].lower() or product_filter == str(v['product_id'])]
        print(f"Filtrando por '{product_filter}': {len(videos)} vídeos selecionados de {len(all_videos)}.")
        if not videos:
            print(f"Nenhum vídeo encontrado para o filtro '{product_filter}'.")
            return None
    else:
        videos = all_videos
        print(f"Iniciando varredura Sentinel completa: {len(videos)} vídeos.")

    results = []
    print(f"Disparando {len(videos)} sondagens HTTP 206 com {max_threads} threads...")

    t_start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(probe_single_video, v, timeout): v for v in videos}
        completed = 0
        for f in as_completed(futures):
            res = f.result()
            results.append(res)
            completed += 1
            if completed % 20 == 0 or completed == len(videos):
                print(f"  Progresso: {completed}/{len(videos)} ({completed*100//len(videos)}%) concluídos...")

    total_time = round(time.perf_counter() - t_start, 2)

    # Se for filtro de produto e estiver gravando no relatório mestre default, faz merge seguro
    final_results = results
    if product_filter and resolved_output == os.path.abspath(DEFAULT_REPORT_PATH) and os.path.exists(resolved_output):
        try:
            with open(resolved_output, 'r', encoding='utf-8') as rf:
                old_report = json.load(rf)
                old_results = old_report.get('results', [])
                results_map = {(r['namespace'], r['video_id']): r for r in old_results}
                for r in results:
                    results_map[(r['namespace'], r['video_id'])] = r
                final_results = list(results_map.values())
                print(f"Merge seguro efetuado: {len(results)} atualizados em {len(final_results)} vídeos totais.")
        except Exception as e:
            print(f"Aviso no merge do relatório anterior: {e}")

    # Ordenar resultados pelo namespace e video_id
    final_results.sort(key=lambda x: (x['namespace'], x['video_id']))

    # Métricas agregadas
    healthy = [r for r in final_results if r['state'] == 'HEALTHY']
    slow = [r for r in final_results if r['state'] == 'SLOW']
    dead = [r for r in final_results if r['state'] == 'DEAD']

    operational_count = len(healthy) + len(slow)
    success_rate = round((operational_count / len(final_results)) * 100, 1) if final_results else 0
    avg_latency = round(sum(r['latency_ms'] for r in final_results) / len(final_results), 1) if final_results else 0
    total_mb_cloud = round(sum(r['total_mb'] for r in final_results), 2)

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_checked": len(final_results),
        "healthy_count": len(healthy),
        "slow_count": len(slow),
        "dead_count": len(dead),
        "operational_count": operational_count,
        "success_rate_percent": success_rate,
        "avg_latency_ms": avg_latency,
        "total_cloud_mb": total_mb_cloud,
        "scan_duration_seconds": total_time
    }

    report = {
        "summary": summary,
        "results": final_results
    }

    os.makedirs(os.path.dirname(resolved_output), exist_ok=True)
    with open(resolved_output, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Relatório Visual no Terminal
    print("\n" + "=" * 60)
    print("           SENTINEL CDN HEALTH REPORT           ")
    print("=" * 60)
    print(f"  Total Monitorado     : {summary['total_checked']}")
    print(f"  Operacionais (206/200): {summary['operational_count']} ({summary['success_rate_percent']}%)")
    print(f"  Status Saudável (OK) : {summary['healthy_count']}")
    print(f"  Status Lento (>1.5s) : {summary['slow_count']}")
    print(f"  Status Offline/Dead  : {summary['dead_count']}")
    print(f"  Latência Média       : {summary['avg_latency_ms']} ms")
    print(f"  Armazenamento Nuvem  : ~{summary['total_cloud_mb']} MB")
    print(f"  Duração da Varredura : {summary['scan_duration_seconds']}s")
    print("=" * 60)
    print(f"Relatório exportado para: {output_path}")

    return report

def main():
    parser = argparse.ArgumentParser(description="Sentinel Catbox CDN Health-Check")
    parser.add_argument('--all', action='store_true', help="Varre todos os 141 vídeos")
    parser.add_argument('--product', type=str, help="Filtra por namespace ou ID do produto (ex: churrasqueira-arke)")
    parser.add_argument('--threads', type=int, default=15, help="Número de threads simultâneas (padrão: 15)")
    parser.add_argument('--timeout', type=int, default=10, help="Timeout em segundos por requisição (padrão: 10)")
    parser.add_argument('--output', type=str, default=DEFAULT_REPORT_PATH, help="Caminho do arquivo de saída JSON")

    parser.add_argument('--strict', action='store_true', help="Retorna exit code 1 se houver vídeos DEAD")

    args = parser.parse_args()

    prod_filter = args.product if args.product else None
    rep = run_sentinel_scan(product_filter=prod_filter, max_threads=args.threads, timeout=args.timeout, output_path=args.output)
    if args.strict and rep and rep.get('summary', {}).get('dead_count', 0) > 0:
        sys.exit(1)

if __name__ == '__main__':
    main()
