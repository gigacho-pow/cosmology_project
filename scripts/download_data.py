"""초신성·BAO 자료 준비. 이미 있는 파일은 덮어쓰지 않는다."""

from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SN_URL = (
    "https://raw.githubusercontent.com/PantheonPlusSH0ES/"
    "DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/"
)
BAO_URL = (
    "https://raw.githubusercontent.com/CobayaSampler/"
    "bao_data/master/desi_bao_dr2/"
)
SOURCES = {
    "Pantheon+SH0ES.dat": SN_URL + "Pantheon+SH0ES.dat",
    "Pantheon+SH0ES_STATONLY.cov": SN_URL + "Pantheon+SH0ES_STATONLY.cov",
    "Pantheon+SH0ES_STAT+SYS.cov": SN_URL + "Pantheon+SH0ES_STAT+SYS.cov",
    "Pantheon_README.txt": SN_URL + "README",
    "bao/desi_gaussian_bao_ALL_GCcomb_mean.txt":
        BAO_URL + "desi_gaussian_bao_ALL_GCcomb_mean.txt",
    "bao/desi_gaussian_bao_ALL_GCcomb_cov.txt":
        BAO_URL + "desi_gaussian_bao_ALL_GCcomb_cov.txt",
}


def main():
    for name, url in SOURCES.items():
        path = ROOT / "data" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            continue
        temporary = path.with_suffix(path.suffix + ".part")
        subprocess.run(
            [
                "curl", "-fL", "--retry", "3", "--connect-timeout", "20",
                "--max-time", "300", url, "-o", str(temporary),
            ],
            check=True,
        )
        temporary.replace(path)


if __name__ == "__main__":
    main()
