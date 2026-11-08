#!/usr/bin/env python3
"""
Scraping Proxy TCO & Retry Bloat Estimator.
Zero-dependency CLI tool utilizing exact Decimal arithmetic.
"""
import sys
import argparse
from decimal import Decimal, ROUND_HALF_UP

def estimate_tco(target_gb: Decimal, failure_rate_pct: Decimal, rate_per_gb: Decimal):
    effective_multiplier = Decimal('1.0') + (failure_rate_pct / (Decimal('100') - failure_rate_pct))
    actual_gb = (target_gb * effective_multiplier).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
    nominal_cost = (target_gb * rate_per_gb).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    real_cost = (actual_gb * rate_per_gb).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    retry_loss = (real_cost - nominal_cost).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return {
        'actual_gb_consumed': actual_gb,
        'nominal_cost': nominal_cost,
        'real_cost': real_cost,
        'retry_waste': retry_loss
    }

def main():
    parser = argparse.ArgumentParser(description="Proxy Scraping TCO & Retry Waste Calculator")
    parser.add_argument('--target-gb', type=Decimal, default=Decimal('100'), help='Nominal payload bandwidth in GB')
    parser.add_argument('--failure-rate', type=Decimal, default=Decimal('20.0'), help='Anti-bot block/retry rate percentage')
    parser.add_argument('--rate-per-gb', type=Decimal, default=Decimal('4.00'), help='Proxy rate in USD/GB')
    args = parser.parse_args()

    res = estimate_tco(args.target_gb, args.failure_rate, args.rate_per_gb)
    print("=== Scraping Proxy TCO Analysis ===")
    print(f"Target Bandwidth:        {args.target_gb} GB")
    print(f"Retry/Block Rate:        {args.failure_rate}%")
    print(f"Actual Traffic Billed:   {res['actual_gb_consumed']} GB")
    print(f"Expected Nominal Cost:   ${res['nominal_cost']}")
    print(f"True Real Cost:          ${res['real_cost']}")
    print(f"Retry Waste Overhead:    ${res['retry_waste']}")

if __name__ == '__main__':
    main()
