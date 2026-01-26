import argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    try:
        import yaml
    except ImportError:
        raise SystemExit("Missing dependency: pyyaml. Install with: pip install pyyaml")

    with open(args.config, "r") as f:
        cfg = yaml.safe_load(f)

    print("Loaded locked config:")
    for k in ["seed", "n_splits", "n_boot", "n_perm"]:
        print(f"  {k}: {cfg[k]}")

    print("\nPaths:")
    for k, v in cfg["paths"].items():
        print(f"  {k}: {v}")

    print("\nFeature sets:")
    print("  Cov3:", cfg["features"]["cov3"])
    print("  CovPP extras:", cfg["features"]["covpp_extra"])

    print("\nTIHM residualization:")
    print(cfg["tihm_residualization"])

    print("\nNOTE: Replace this scaffold with the actual evaluation pipeline scripts used to generate the paper results.")
    print("This repo exists to make protocol + descriptor definitions explicit for reviewers.")

if __name__ == "__main__":
    main()
