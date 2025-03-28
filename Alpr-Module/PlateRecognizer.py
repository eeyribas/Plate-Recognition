from openalpr import Alpr

alpr=Alpr("eu", "/home/pi/openalpr/config/openalpr.conf", "/home/pi/openalpr/runtime_data")
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)
    
alpr.set_top_n(1)
results=alpr.recognize_file("image.jpg")

i=0
for plate in results['results']:
    i+=1
    print("Plate : #%d" % i)
    for candidate in plate['candidates']:
        prefix="-"
        if candidate['matches_template']:
            prefix="*"
        print("%12s" % ( candidate['plate']))

alpr.unload()