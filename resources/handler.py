import mapnik
from mapnik import Image
from fastapi import FastAPI, Response
from mangum import Mangum

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, url: str = None):
    return {"item_id": item_id, "q": url}

@app.get("/items/{item_id}")
def read_item(item_id: int, url: str = None):
    return {"item_id": item_id, "q": url}

@app.get("/tile/{z}/{x}/{y}")
def read_tile(z: int, x: int, y: int, url: str = None):
    m = mapnik.Map(256, 256) # create a map with a given width and height in pixels
    bounds = mapnik.Box2d(-9256829.873448031,5225846.749800993,-9255606.88099547,5227069.742253557)
    m.maximum_extent = bounds
    s = mapnik.Style() # style object to hold rules
    r = mapnik.Rule() # rule object to hold symbolizers
    polygon_symbolizer = mapnik.PolygonSymbolizer()
    polygon_symbolizer.fill = mapnik.Color('#f2eff9')
    r.symbols.append(polygon_symbolizer) # add the symbolizer to the rule object
    line_symbolizer = mapnik.LineSymbolizer()
    line_symbolizer.stroke = mapnik.Color('rgb(50%,50%,50%)')
    line_symbolizer.stroke_width = 0.1
    r.symbols.append(line_symbolizer) # add the symbolizer to the rule object
    s.rules.append(r) # now add the rule to the style and we're done
    m.append_style('My Style',s) # Styles are given names only as they are applied to the map
    ds = mapnik.Ogr(file='/vsicurl/https://pul-tile-images.s3.amazonaws.com/detroit-parcels.pmtiles', layer_by_index=0)
    layer = mapnik.Layer('world') # new layer called 'world' (we could name it
    layer.datasource = ds
    layer.styles.append('My Style')
    m.layers.append(layer)
    m.zoom_all()
    im = Image(m.width,m.height)
    mapnik.render(m, im)
    out = im.tostring('png')
    return Response(content=out, media_type='image/png')

handler = Mangum(app)

