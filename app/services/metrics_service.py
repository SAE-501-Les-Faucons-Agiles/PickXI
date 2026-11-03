import time
import tracemalloc
from typing import Callable, Any, Tuple, List, Dict

class MetricsService:
    """
    Service dédié aux mesures de performances, à l'analyse de complexité
    et au calcul d'impact énergétique (évaluation de la compétence Optimisation).
    """

    def __init__(self):
        # Historique des temps d'exécution pour chaque approche
        self.history: Dict[str, List[float]] = {
            "content_based": [],
            "heuristic_popularity": []
        }

    def measure_execution(
        self,
        func: Callable[..., Any],
        approach_key: str,
        *args,
        iterations: int = 5,
        **kwargs
    ) -> Tuple[Any, float, float, float, float, float]:
        """
        Mesure le temps min, max, moyen d'exécution et la consommation mémoire.
        """
        tracemalloc.start()
        run_times = []
        result = None

        for _ in range(iterations):
            start = time.perf_counter()
            res = func(*args, **kwargs)
            duration_ms = (time.perf_counter() - start) * 1000.0
            run_times.append(duration_ms)
            result = res

        current_mem, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Enregistrement dans l'historique
        if approach_key not in self.history:
            self.history[approach_key] = []
        self.history[approach_key].extend(run_times)

        all_times = self.history[approach_key]
        time_min = min(all_times)
        time_max = max(all_times)
        time_avg = sum(all_times) / len(all_times)
        last_time = run_times[-1]
        memory_kb = peak_mem / 1024.0

        return result, last_time, time_min, time_max, time_avg, memory_kb

    def estimate_battery_impact(self, exec_time_ms: float, memory_kb: float) -> str:
        """
        Estimation qualitative de l'impact batterie pour le rapport d'optimisation.
        """
        if exec_time_ms < 1.0 and memory_kb < 50.0:
            return "Très faible (Éco-optimisé)"
        elif exec_time_ms < 5.0 and memory_kb < 200.0:
            return "Faible (Acceptable mobile)"
        elif exec_time_ms < 15.0:
            return "Moyen (Consommation modérée)"
        else:
            return "Élevé (Nécessite optimisation / mise en cache)"

# Instance singleton du service de métriques
metrics_service = MetricsService()
