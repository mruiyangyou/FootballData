# "footballdata"

It's under development(will be published into a python library can be downloaded by **Pip**)and will acheive more methods to web scrape from this website: <https://www.football-data.co.uk/englandm.php>. Currently it can be accessed for England leagues' data. Later more countries and leagues will be available.

## Methods
The current methods for obejct **FootballData**:
* Scrape one season data - match stats
* Scrape multiple seasons - match stats
* Scrape particular team data - team stats

## Sample

### Import 

`imoprt footballdata as fd`

### Use

```
country, league = 'xx', 'xx' 
db = fdd.FootballData(country, league)
```

More details can be accessed from the [test notebook](test.ipynb).