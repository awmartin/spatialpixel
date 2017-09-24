
# List of public map tile Z/X/Y map tile servers.
tile_servers = {
    # http://maps.stamen.com/
    'toner'              : "http://tile.stamen.com/toner/%s/%s/%s.png",
    'toner-lines'        : "http://tile.stamen.com/toner-lines/%s/%s/%s.png",
    'toner-hybrid'       : "http://tile.stamen.com/toner-hybrid/%s/%s/%s.png",
    'toner-background'   : "http://tile.stamen.com/toner-background/%s/%s/%s.png",
    'toner-lite'         : "http://tile.stamen.com/toner-lite/%s/%s/%s.png",
    'terrain'            : "http://tile.stamen.com/terrain/%s/%s/%s.png",
    'terrain-lines'      : "http://tile.stamen.com/terrain-lines/%s/%s/%s.png",
    'terrain-background' : "http://tile.stamen.com/terrain-background/%s/%s/%s.png",
    'watercolor'         : "http://tile.stamen.com/watercolor/%s/%s/%s.png",

    # Found in https://github.com/dfacts/staticmaplite/blob/master/staticmap.php
    'mapnik'             : "http://tile.openstreetmap.org/%s/%s/%s.png",
    'cycle'              : "http://a.tile.opencyclemap.org/cycle/%s/%s/%s.png",

    # http://wiki.openstreetmap.org/wiki/Tile_servers
    'openstreetmap'      : "http://a.tile.openstreetmap.org/%s/%s/%s.png", # also http://b.* and https://c.*
    'wikimedia'          : "https://maps.wikimedia.org/osm-intl/%s/%s/%s.png",
    'carto-light'        : "http://a.basemaps.cartocdn.com/light_all/%s/%s/%s.png",
    'carto-dark'         : "http://a.basemaps.cartocdn.com/dark_all/%s/%s/%s.png",
    'openptmap'          : "http://www.openptmap.org/tiles/%s/%s/%s.png",
    'hikebike'           : "http://a.tiles.wmflabs.org/hikebike/%s/%s/%s.png",

    # https://carto.com/location-data-services/basemaps/
    # Note: These seem to be really slow.
    'carto-lightall'     : "http://cartodb-basemaps-1.global.ssl.fastly.net/light_all/%s/%s/%s.png",
    'carto-darkall'      : "http://cartodb-basemaps-1.global.ssl.fastly.net/dark_all/%s/%s/%s.png",
    'carto-lightnolabels': "http://cartodb-basemaps-1.global.ssl.fastly.net/light_nolabels/%s/%s/%s.png",
    'carto-darknolabels' : "http://cartodb-basemaps-1.global.ssl.fastly.net/dark_nolabels/%s/%s/%s.png",
    }
