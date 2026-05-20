import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


RULE_TEXTS = [
    "IF çalışma süresi Az AND uyku İyi AND aktivite Yüksek AND stres Düşük THEN verimlilik Çok Yüksek",
    "IF çalışma süresi Normal AND uyku İyi AND aktivite Yüksek AND stres Düşük THEN verimlilik Çok Yüksek",
    "IF çalışma süresi Normal AND uyku Orta AND aktivite Yüksek AND stres Düşük THEN verimlilik Yüksek",
    "IF çalışma süresi Normal AND uyku İyi AND aktivite Orta AND stres Orta THEN verimlilik Yüksek",
    "IF çalışma süresi Fazla AND uyku İyi AND aktivite Yüksek AND stres Düşük THEN verimlilik Yüksek",
    "IF çalışma süresi Fazla AND uyku Kötü AND aktivite Düşük AND stres Yüksek THEN verimlilik Çok Düşük",
    "IF çalışma süresi Fazla AND uyku Kötü AND stres Yüksek THEN verimlilik Çok Düşük",
    "IF çalışma süresi Fazla AND aktivite Düşük AND stres Orta THEN verimlilik Düşük",
    "IF çalışma süresi Az AND uyku Kötü AND aktivite Düşük THEN verimlilik Düşük",
    "IF çalışma süresi Az AND uyku İyi AND aktivite Düşük THEN verimlilik Orta",
    "IF çalışma süresi Normal AND uyku Orta AND aktivite Orta AND stres Orta THEN verimlilik Orta",
    "IF çalışma süresi Normal AND uyku Kötü AND stres Yüksek THEN verimlilik Düşük",
    "IF uyku İyi AND aktivite Yüksek AND stres Düşük THEN verimlilik Çok Yüksek",
    "IF uyku Kötü AND stres Yüksek THEN verimlilik Çok Düşük",
    "IF aktivite Yüksek AND stres Orta AND çalışma süresi Normal THEN verimlilik Yüksek",
    "IF aktivite Düşük AND stres Yüksek THEN verimlilik Düşük",
    "IF çalışma süresi Fazla AND uyku Orta AND aktivite Orta THEN verimlilik Orta",
    "IF çalışma süresi Az AND aktivite Orta AND stres Düşük THEN verimlilik Orta",
    "IF çalışma süresi Normal AND uyku İyi AND stres Yüksek THEN verimlilik Orta",
    "IF çalışma süresi Fazla AND uyku İyi AND stres Orta THEN verimlilik Orta",
]


def create_fuzzy_system():
    work_hours = ctrl.Antecedent(np.arange(0, 13, 1), "work_hours")
    sleep_hours = ctrl.Antecedent(np.arange(0, 11, 1), "sleep_hours")
    activity = ctrl.Antecedent(np.arange(0, 101, 1), "activity")
    stress = ctrl.Antecedent(np.arange(0, 101, 1), "stress")

    productivity = ctrl.Consequent(np.arange(0, 101, 1), "productivity")

    work_hours["low"] = fuzz.trimf(work_hours.universe, [0, 0, 4])
    work_hours["normal"] = fuzz.trimf(work_hours.universe, [3, 6, 8])
    work_hours["high"] = fuzz.trimf(work_hours.universe, [7, 12, 12])

    sleep_hours["bad"] = fuzz.trimf(sleep_hours.universe, [0, 0, 5])
    sleep_hours["medium"] = fuzz.trimf(sleep_hours.universe, [4, 6, 8])
    sleep_hours["good"] = fuzz.trimf(sleep_hours.universe, [7, 10, 10])

    activity["low"] = fuzz.trimf(activity.universe, [0, 0, 40])
    activity["medium"] = fuzz.trimf(activity.universe, [30, 50, 70])
    activity["high"] = fuzz.trimf(activity.universe, [60, 100, 100])

    stress["low"] = fuzz.trimf(stress.universe, [0, 0, 40])
    stress["medium"] = fuzz.trimf(stress.universe, [30, 50, 70])
    stress["high"] = fuzz.trimf(stress.universe, [60, 100, 100])

    productivity["very_low"] = fuzz.trimf(productivity.universe, [0, 0, 25])
    productivity["low"] = fuzz.trimf(productivity.universe, [15, 30, 45])
    productivity["medium"] = fuzz.trimf(productivity.universe, [35, 50, 65])
    productivity["high"] = fuzz.trimf(productivity.universe, [55, 70, 85])
    productivity["very_high"] = fuzz.trimf(productivity.universe, [75, 100, 100])

    rules = [
        ctrl.Rule(work_hours["low"] & sleep_hours["good"] & activity["high"] & stress["low"], productivity["very_high"]),
        ctrl.Rule(work_hours["normal"] & sleep_hours["good"] & activity["high"] & stress["low"], productivity["very_high"]),
        ctrl.Rule(work_hours["normal"] & sleep_hours["medium"] & activity["high"] & stress["low"], productivity["high"]),
        ctrl.Rule(work_hours["normal"] & sleep_hours["good"] & activity["medium"] & stress["medium"], productivity["high"]),
        ctrl.Rule(work_hours["high"] & sleep_hours["good"] & activity["high"] & stress["low"], productivity["high"]),

        ctrl.Rule(work_hours["high"] & sleep_hours["bad"] & activity["low"] & stress["high"], productivity["very_low"]),
        ctrl.Rule(work_hours["high"] & sleep_hours["bad"] & stress["high"], productivity["very_low"]),
        ctrl.Rule(work_hours["high"] & activity["low"] & stress["medium"], productivity["low"]),
        ctrl.Rule(work_hours["low"] & sleep_hours["bad"] & activity["low"], productivity["low"]),
        ctrl.Rule(work_hours["low"] & sleep_hours["good"] & activity["low"], productivity["medium"]),

        ctrl.Rule(work_hours["normal"] & sleep_hours["medium"] & activity["medium"] & stress["medium"], productivity["medium"]),
        ctrl.Rule(work_hours["normal"] & sleep_hours["bad"] & stress["high"], productivity["low"]),
        ctrl.Rule(sleep_hours["good"] & activity["high"] & stress["low"], productivity["very_high"]),
        ctrl.Rule(sleep_hours["bad"] & stress["high"], productivity["very_low"]),
        ctrl.Rule(activity["high"] & stress["medium"] & work_hours["normal"], productivity["high"]),

        ctrl.Rule(activity["low"] & stress["high"], productivity["low"]),
        ctrl.Rule(work_hours["high"] & sleep_hours["medium"] & activity["medium"], productivity["medium"]),
        ctrl.Rule(work_hours["low"] & activity["medium"] & stress["low"], productivity["medium"]),
        ctrl.Rule(work_hours["normal"] & sleep_hours["good"] & stress["high"], productivity["medium"]),
        ctrl.Rule(work_hours["high"] & sleep_hours["good"] & stress["medium"], productivity["medium"]),
    ]

    system = ctrl.ControlSystem(rules)

    variables = {
        "work_hours": work_hours,
        "sleep_hours": sleep_hours,
        "activity": activity,
        "stress": stress,
        "productivity": productivity,
        "rules": rules,
    }

    return system, variables


def get_membership_degree(variable, term, value):
    return fuzz.interp_membership(
        variable.universe,
        variable[term].mf,
        value
    )


def get_active_rules(work_value, sleep_value, activity_value, stress_value):
    system, variables = create_fuzzy_system()

    work = variables["work_hours"]
    sleep = variables["sleep_hours"]
    activity = variables["activity"]
    stress = variables["stress"]

    degrees = {
        "work_low": get_membership_degree(work, "low", work_value),
        "work_normal": get_membership_degree(work, "normal", work_value),
        "work_high": get_membership_degree(work, "high", work_value),

        "sleep_bad": get_membership_degree(sleep, "bad", sleep_value),
        "sleep_medium": get_membership_degree(sleep, "medium", sleep_value),
        "sleep_good": get_membership_degree(sleep, "good", sleep_value),

        "activity_low": get_membership_degree(activity, "low", activity_value),
        "activity_medium": get_membership_degree(activity, "medium", activity_value),
        "activity_high": get_membership_degree(activity, "high", activity_value),

        "stress_low": get_membership_degree(stress, "low", stress_value),
        "stress_medium": get_membership_degree(stress, "medium", stress_value),
        "stress_high": get_membership_degree(stress, "high", stress_value),
    }

    rule_strengths = [
        min(degrees["work_low"], degrees["sleep_good"], degrees["activity_high"], degrees["stress_low"]),
        min(degrees["work_normal"], degrees["sleep_good"], degrees["activity_high"], degrees["stress_low"]),
        min(degrees["work_normal"], degrees["sleep_medium"], degrees["activity_high"], degrees["stress_low"]),
        min(degrees["work_normal"], degrees["sleep_good"], degrees["activity_medium"], degrees["stress_medium"]),
        min(degrees["work_high"], degrees["sleep_good"], degrees["activity_high"], degrees["stress_low"]),

        min(degrees["work_high"], degrees["sleep_bad"], degrees["activity_low"], degrees["stress_high"]),
        min(degrees["work_high"], degrees["sleep_bad"], degrees["stress_high"]),
        min(degrees["work_high"], degrees["activity_low"], degrees["stress_medium"]),
        min(degrees["work_low"], degrees["sleep_bad"], degrees["activity_low"]),
        min(degrees["work_low"], degrees["sleep_good"], degrees["activity_low"]),

        min(degrees["work_normal"], degrees["sleep_medium"], degrees["activity_medium"], degrees["stress_medium"]),
        min(degrees["work_normal"], degrees["sleep_bad"], degrees["stress_high"]),
        min(degrees["sleep_good"], degrees["activity_high"], degrees["stress_low"]),
        min(degrees["sleep_bad"], degrees["stress_high"]),
        min(degrees["activity_high"], degrees["stress_medium"], degrees["work_normal"]),

        min(degrees["activity_low"], degrees["stress_high"]),
        min(degrees["work_high"], degrees["sleep_medium"], degrees["activity_medium"]),
        min(degrees["work_low"], degrees["activity_medium"], degrees["stress_low"]),
        min(degrees["work_normal"], degrees["sleep_good"], degrees["stress_high"]),
        min(degrees["work_high"], degrees["sleep_good"], degrees["stress_medium"]),
    ]

    active_rules = []

    for index, strength in enumerate(rule_strengths):
        if strength > 0:
            active_rules.append({
                "Kural No": index + 1,
                "Kural": RULE_TEXTS[index],
                "Aktivasyon": round(float(strength), 3)
            })

    return active_rules, degrees


def calculate_productivity(work_hours_value, sleep_hours_value, activity_value, stress_value):
    system, variables = create_fuzzy_system()
    simulation = ctrl.ControlSystemSimulation(system)

    simulation.input["work_hours"] = work_hours_value
    simulation.input["sleep_hours"] = sleep_hours_value
    simulation.input["activity"] = activity_value
    simulation.input["stress"] = stress_value

    active_rules, degrees = get_active_rules(
        work_hours_value,
        sleep_hours_value,
        activity_value,
        stress_value
    )

    try:
        simulation.compute()
        result = simulation.output.get("productivity", 50)
    except Exception:
        result = 50

    return round(result, 2), variables, active_rules, degrees