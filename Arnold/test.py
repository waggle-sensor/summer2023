from  sage_data_client import query

data =query(
    start= "2023-05-10T01:00:00Z",
  end= "2023-06-10T01:00:00Z",
  filter = {
    "name" : "upload",
        "vsn": "W083",
        "plugin" : "registry.sagecontinuum.org/theone/imagesampler:0.3.0",
	"task" : "imagesampler-bottom"
	
    }
)
print(data['timestamp'])