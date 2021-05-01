import requests

#base URL used for API Calls
def get_base_URL():
    return "https://api-v3.mbta.com"

#get list of routes based on string 
#input: must be a string representing type of routes (i.e light, heavy)
def get_routes(filter_type):
    if type(filter_type) != str:
        raise ValueError("Filter type must be string.")

    p = {"filter[type]": filter_type}
    all_routes_list = requests.get(get_base_URL() + "/routes", params=p).json() #API CALL
    all_routes = all_routes_list['data']

    return all_routes

#get list of stops based on input route_id
#input: route_id is string type
def get_stops(route_id):
    if type(route_id) != str:
        raise ValueError("Route ID must be a string")

    p = {"filter[route]": route_id}
    all_stops = requests.get(get_base_URL() + "/stops", params=p).json() #API CALL
    stops = all_stops['data']

    return stops


#get list of directions based on input route_id
#input: route_id is string type
def get_directions(route_id):
    if type(route_id) != str:
        raise ValueError("Route ID must be string.")

    p = {"filter[id]": route_id}
    curr_route_data = requests.get(get_base_URL() + "/routes", params=p).json() #API CALL
    curr_route = curr_route_data['data'][0]
    directions = curr_route['attributes']['direction_names']
    directions = [direction.lower() for direction in directions]

    return directions

#get list of predictions based on route_id, stop_id, direction_id  
def get_predictions(route_id, stop_id, direction_id):
    if type(route_id) != str or type(stop_id) != str or type(direction_id) != int:
        raise ValueError('Input IDs are not all correct types.')

    #sort list of predictions by departure time
    p = {"filter[route]": route_id, "filter[stop]": stop_id, "filter[direction_id]" : direction_id}
    predictions = requests.get(get_base_URL() + "/predictions" + "?sort=departure_time", params=p).json() #API CALL

    return predictions

#get long_name of route, grab corresponding route_id
def name_to_route_id(selected_route, all_routes):
    route_id = ''
    for route in all_routes:
        if selected_route.lower() == route['attributes']['long_name'].lower():
            route_id = route['id']
    
    return route_id

#get name of stop, grab corresponding stop_id
def name_to_stop_id(selected_stop, stops):
    stop_id = ''
    for stop in stops:
        if selected_stop.lower() == stop['attributes']['name'].lower():
            stop_id = stop['id']
    
    return stop_id


#get name of direction, grab corresponding direction_id
def name_to_direction_id(selected_direction, directions):
    direction_id = -1

    #direction_id derived from index of the directions_list
    for i in range(len(directions)):
        if directions[i].lower() == selected_direction.lower():
            direction_id = i
            break

    return direction_id

#get next departure time
def get_next_departure_time(predictions):
    next_predicted_time = ""

    #look through list of predictions, look for first instance of a non-none time
    for prediction in predictions['data']:
        if prediction['attributes']['departure_time'] is not None:
            next_predicted_time = prediction['attributes']['departure_time']
            break

    return next_predicted_time

#main method, simulate the program to the user
def main():

    #start program
    while(1):
        
        print("")
        print("Welcome! Find the next departing train!")
        print("")
        print("-----ROUTES-----")

        #get list of routes of light and heavy rail trains
        filter_type = "0,1"
        all_routes = get_routes(filter_type)
        
        route_names = []
        for route in all_routes:
            print(route['attributes']['long_name'])
            route_names.append(route['attributes']['long_name'].lower())

        print("----------------")
        

        #get user's route, make sure it is valid input
        selected_route = input("Please type in your route: ")
        while selected_route.lower() not in route_names:
            selected_route = input("Invalid input! Please type in your route: ")

        route_id = name_to_route_id(selected_route, all_routes)


        print("")
        print("------STOPS-------")

        #get list of stops 
        stops = get_stops(route_id)
        stop_names = []
        for stop in stops:
            print(stop['attributes']['name'])
            stop_names.append(stop['attributes']['name'].lower())

        print("------------------")
     
        # get user's stop, make sure it is valid
        selected_stop = input("Please type in your stop: ")
        while selected_stop.lower() not in stop_names:
            selected_stop = input("Invalid input! Please type in your stop: ")

        #get corresponding id
        stop_id = name_to_stop_id(selected_stop, stops)
        
        print("")
        print("------DIRECTIONS------")

        #display list of directions, print them
        directions = get_directions(route_id)
        for direction in directions:
            print(direction.capitalize())
        print("----------------------")

        #get user's selected direction, convert to corresponding direction id
        selected_direction = input("Please type in your direction: ")
        while selected_direction.lower() not in directions:
            selected_direction = input("Invalid input! Please type in your direction: ")
        direction_id = name_to_direction_id(selected_direction, directions)
        
        
        #get all predictions with previous inputs as filters
        predictions = get_predictions(route_id, stop_id, direction_id)
        next_predicted_time = get_next_departure_time(predictions)
        print("")


        #check if a departure time was found, print result to user 
        if next_predicted_time == "":
            print("There is currently no departure time for your specified requirements.")
            
        else:
            print("The next departure time is {}".format(next_predicted_time))

        #ask user if they want to quit
        print("")
        print("Would you like to quit?")
        print("Type q to quit. Press any other key to start over.")

        answer = input("Your answer: ")

        if answer == 'Q' or answer == 'q':
            break

if __name__ == "__main__":
    main()
