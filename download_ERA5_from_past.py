# %%
import datetime
import os
import sys
from pathlib import Path
import cdsapi
import logging


logging.getLogger("cdsapi").setLevel(logging.WARNING)


# %%


def download_data(
    Start_day,
    End_day,
    out_folder_netcdf_hourly,
    c,
    hours,
    bbox,
):
    delta = End_day - Start_day
    for i in range(delta.days):
        day2download = End_day - datetime.timedelta(days=i)

        out_prec_nc_hourly = (
            out_folder_netcdf_hourly
            / "{}{:02d}{:02d}_ERA5_prec.nc".format(
                day2download.year, day2download.month, day2download.day
            )
        )

        # download
        if not out_prec_nc_hourly.exists():
            print(f"downloading prec data for: {day2download}")
            c.retrieve(
                "reanalysis-era5-land",
                {
                    "variable": [
                        "total_precipitation",
                        "runoff",
                        "potential_evaporation",
                    ],
                    "product_type": "reanalysis",
                    "year": day2download.year,
                    "month": day2download.month,
                    "day": [day2download.day],
                    "time": hours,
                    "area": bbox,
                    "format": "netcdf",
                },
                out_prec_nc_hourly,
            )


def main():
    Start_day = datetime.datetime(1980, 1, 1)
    End_day = datetime.datetime(2020, 1, 1)  # month is first

    Out_folder_netcdf_hourly = Path(r"V:\Canada\ERA5\Frazer\out_netcdf_hourly")

    proxy = "http://aonid:password@10.1.123.16:8888"
    os.environ["http_proxy"] = proxy
    os.environ["https_proxy"] = proxy

    Hours = [
        "00:00",
        "01:00",
        "02:00",
        "03:00",
        "04:00",
        "05:00",
        "06:00",
        "07:00",
        "08:00",
        "09:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
        "18:00",
        "19:00",
        "20:00",
        "21:00",
        "22:00",
        "23:00",
    ]
    # Fraser river
    north = 57
    west = -128
    south = 48
    east = -118

    BBox = [north, west, south, east]

    Out_folder_netcdf_hourly.mkdir(parents=True, exist_ok=True)

    try:
        C = cdsapi.Client(timeout=600, quiet=False, debug=True)
        print("Connection prepared")
    except Exception as e:
        sys.exit(-1)

    download_data(
        Start_day,
        End_day,
        Out_folder_netcdf_hourly,
        C,
        Hours,
        BBox,
    )


if __name__ == "__main__":
    main()

# %%
