# Hold off on prophet image generation, probably not useful since I buy small caps

import sys 
import argparse as ap
import pathlib
import glob
import shutil
from jinja2 import Template
from datetime import date, datetime
from stocks.util import get_config
from stocks.report import make_risk_metrics, \
    make_performance_plot, make_estimated_returns, \
    make_portfolio_allocations

def main(args):
    end_date = str(date.today())
    gh_pages_name = 'gh-pages'
    for report_cfg_file in glob.glob("stocks/cfg/*.yml"):
        report_cfg = get_config(report_cfg_file)
        options = dict(Version="1.0.0", CurrDate=end_date)
        stocks = report_cfg["stocks"]
        weights = report_cfg["weights"]
        start_date = report_cfg["start_date"]
        report_name = report_cfg["name"]
        
        # Relative paths to performance images,
        # images are in the same directory as index.html
        output_folder = f"{args.output}/{report_name}"
        pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)

        if isinstance(weights, str):
            # set equal list based on stock length
            # TODO add more types later
            weights = [1.00 / len(stocks)] * len(stocks)
            risk_metrics = make_risk_metrics(stocks, weights, start_date, end_date)
        else:
            risk_metrics = make_risk_metrics(stocks, weights, start_date, end_date)
        # Add Var, VaR, CVaR, CDaR
        options["RISK_METRICS"] = risk_metrics
        options["ESTIMATED_RETURNS"] = make_estimated_returns(stocks, start_date, end_date)
        performance_images = []
        image_name = f"{start_date}_{end_date}_basic.png"
        plot_made = make_performance_plot(
            stocks,
            start_date=start_date,
            end_date=end_date,
            file_name=f"{output_folder}/{image_name}"
        )
        if plot_made is not None:
            performance_images.append(image_name)
        else:
            print(f"PLOT NOT MADE for {image_name} for {report_name}")
        options["PERFORMANCE_IMAGES"] = performance_images

        # Adding weights optimization
        if "portfolio_opt" in report_cfg:
            portfolio_opt = report_cfg["portfolio_opt"]
            # Get prices for stocks, if I ever get to rebuilding this
            # pass in stock prices once, not a huge deal, not time sensitive issue
            portfolio_allocations = make_portfolio_allocations(
                stocks,
                portfolio_opt,
                start_date,
                end_date
            )
            options["PORTFOLIO_ALLOCATIONS"] = portfolio_allocations
            # iterate across the portfolio
        with open(args.template) as file_:
            template = Template(file_.read())
        renderer_template = template.render(**options)
        with open(f"{output_folder}/index.html", "w", errors='ignore') as f:
            f.write(renderer_template)

        # Attempt to move the folder
        # Make in gh pages folder even if exists
        gh_report_folder = f"{args.output}/{gh_pages_name}/{report_name}/{end_date}"
        pathlib.Path(gh_report_folder).mkdir(parents=True, exist_ok=True)
        # Any files in the output folder, if I need nested files in folders
        # use something else
        for report_file in glob.glob(f"{output_folder}/*"):
            try:
                shutil.move(report_file, gh_report_folder)
            except shutil.Error as e:
                print(e)
        # Could make into another function
    
if __name__ == "__main__":
    assert sys.version_info >= (3, 6)
    startTime = datetime.now()
    parser = ap.ArgumentParser()
    parser.add_argument("-o",
                        "--output",
                        help="Output folder",
                        default="report")
    parser.add_argument("-t", 
                        "--template", 
                        help="Template file", 
                        default="stocks/cfg/template.jinja2") 
    args = parser.parse_args()
    main(args)
    print("Script Complete")
    print(datetime.now() - startTime)
