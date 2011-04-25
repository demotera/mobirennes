#MUMORO CONFIGURATION BEFORE LAUNCHING SERVER

#Database type, choose among : 'sqlite', 'mysql', 'postgres', 'oracle', 'mssql', and 'firebird'
db_type = 'sqlite'

#Database connexion URL
#For user oriented databases : 'username:password@host:port/database'
#Port can be excluded (default one depending on db_type will be used) : 'username:password@host/database'
#For SQLiTE : 'file_name.db' for relative path or absolute : '/data/guidage/file_name.db'
db_params = 'rennesGTFS2.sqlite'

#Load street data from (compressed or not) osm file(s)
#-----------------------------------------------------
osm_data = import_street_data( 'rennes.osm' )

#Load bike service from an API URL (Don't forget to add http://) with required valid params (depending on each API)
#------------------------------------------------------------------------------------------------------------------
data_bike = import_bike_service('http://data.keolis-rennes.com/xml/?version=1.0&key=6D0RGK6K94FYNI6&cmd=getstation&param[request]=all', 
                                 'Le velo STAR')


#Loads muncipal data file and inserts it into database.
#starting_date & end_date in this format : 'YYYYMMDD' Y for year's digists, M for month's and D for day's
#starting_date and end_date MUST be defined if municipal data is imported
#------------------------------------------------------------------------------------------------------------------

start_date = '20110425'
end_date = '20110701'

star_data = import_gtfs_data('GTFS-20110325.zip', 'Metro Bus STAR')
metro_data = import_freq_data('Metro a', 'data_rennes/metro/nodes.csv', 'data_rennes/metro/edges.csv', start_date, end_date)

#Create relevant layers from previously imported data (origin paramater) with a name, a color and the mode.
#Color in the html format : '#RRGGBB' with R, G and B respetcly reg, green and blue values in hex
#Mode choose among: mumoro.Foot, mumoro.Bike and mumoro.Car 
#For GTFS Municipal layer dont mention layer mode
#--------------------------------------------------------------------------------------------------------------------
foot_layer = street_layer( data=osm_data , name='Foot', color='#7E2217', mode=mumoro.Foot )
bike_layer = street_layer( data=osm_data, name='Bike', color='#652AF7', mode=mumoro.Bike, bike_service=data_bike )
star_layer = public_transport_layer(data=star_data ,name='STAR', color='#4CC417' )
metro_layer = public_transport_layer(data=metro_data ,name='Metro', color='#F00BA4' )

#Starting layer is the layer on wich the route begins
#Destination layer is the layer on wich the route finishes
#Starting & destination layers MUST be selected, otherwise the server could not start
#If by mistake you select more than one starting/destination layers, the affectation will go on the last one
# set_starting_layer( layer )
# set_destination_layer( layer )

#Creates a transit cost variable, including the duration in seconds of the transit and if the mode is changed (True or False)
#------------------------------------------------------------------------------------------------------------
#cost1 = cost( duration , mode_changed )
cost1 = cost( duration = 120, mode_change = True )
cost2 = cost( duration = 60, mode_change = False )
#Connect 2 given layers on same nodes with the given cost(s)
#-----------------------------------------------------------
#connect_layers_same_nodes( layer1 , layer2 , cost )

#Connect 2 given layers on nodes imported from a list (Returned value from import_bike_service or import_municipal_data) with the given cost(s)
#----------------------------------------------------------------------------------------------------------------------------------------------
#connect_layers_from_node_list( layer1, layer2, list, cost1, cost2 )
#Connect 2 given layers on nearest nodes
#----------------------------------------
#connect_layers_on_nearest_nodes( layer1, layer2, cost )

connect_layers_from_node_list( foot_layer, bike_layer, data_bike,cost1, cost2 )
connect_layers_on_nearest_nodes(star_layer, foot_layer, cost1 , cost2)
connect_layers_on_nearest_nodes(metro_layer, foot_layer, cost1 , cost2)


paths( foot_layer, foot_layer, [ mode_change, line_change, penibility ], [300, 120, 4]  )
# paths( star_layer, star_layer, [ dist, mode_change ] )

