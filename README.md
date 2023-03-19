# drag_race_viz

This dashboard is hosted through `Render` here.

## Contributor

- Shaun Hutchinson

## Motivation

This application was created as an extension of the [dragracerviz](https://github.com/UBC-MDS/dragracerviz/). The target audience, persona, and research question of this project can be found [here](https://github.com/UBC-MDS/dragracerviz/blob/main/reports/proposal.md). 

This application extends specifically on the question: Which drag queen has the highest win right across all seasons?. As RuPaul's Drag Race has grown in popularity and budget, we have had the number of queens grow each season, as well as the number of episodes. In season 1, there were only 9 drag queens with a total of 9 episodes, including the reunion episode. Now, on season 14, there were 14 queens for a total of 16 episodes. So, to determine the best drag queen based on number of wins is hard to do since a queen on season 1 would have less opportunity to win episodes than a queen on season 14. As a result, to have a higher accuracy in ranking the queens' performance, it was necessary to compare Drag Queens based on the percentage of episodes they won, were ranked high, safe, low or in the bottom. In addition, there are several queens who have returned on a subsequent season. So, this application looks at how they performed overall on their time on the show.
## App Description

This application gives an overview of how each Drag Queen has performed on RuPaul's Drag Race. The main components of the dashboard will have a bar chart that shows the queens with the highest percentage of the chosen outcome. Below this, there is a data table that contains the number of challenges that each queen won, ranked either high, medium or low, and the number of challenges the queen was in the bottom. This table is sorted by the outcome percentage that the user selects.

To the right of the main panel is the filters that the user can interact with to filter/sort the data for the dashboard. There is a radio button selection for outcome category: `Win Percentage` , `High Percentage` `Safe Percentage`, `Low Percentage`, `Bottom Percentage` . In addition there is a dropdown so that the user can select and compare one or more drag queens.

## Usage

To use the dashboard, simply visit the deployed link and explore the data. Users can hover over the chart for exact outcome percentage information. In addition the data table contains all outcome information for each queen, unless filtered for certain queens in particular. 

To interact with the dashboard simply select one of the outcome categories other than the default `Win Percentage`. Additionally users can filter the queens in the visualizations by utalizing the dropdown for queen selection.

Deployed link: 

## References

The main source of the data is from the [dragracer](https://cran.r-project.org/web/packages/dragracer/readme/README.html). This is an R package of data sets that is created from scraping the drag race fandom wiki [wiki](https://rupaulsdragrace.fandom.com/). 

In addition, though not used in this application, the latitude and longitude contained in the cleaned [data set](https://github.com/shaunhutch/drag_race_viz/blob/main/data/drag.csv) in this repo are sourced from [simplemaps.com](https://simplemaps.com/data/us-cities) using their Basic Database.

## Contributing

If you are interested in contributing to this project, please follow these steps:

- Fork the repository and clone it to your local machine.
- Create a new branch for your work.
- Make your changes and commit them with clear commit messages.
- Push your changes to your fork.
- Submit a pull request with a clear description of your changes.

Contributors are welcome to work on any part of the dashboard, including adding new features, improving the user interface, or fixing bugs. If you are looking for ideas for how to contribute, please see the issues section of the repository for a list of current issues that need attention. 
Note that all contributions must abide by our [guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md).


Thank you for your interest in contributing to drag_race_viz!
