# car-assistant-using--llama2

- made a car-assistant ageat using llama-2 that reads obd2 fault codes and gives us a non-technical and user friendly explanation. Retrieves info from a knowledge base in the form a json file with 100 fault codes for now
- learnt rag (retrieval augmented generation) and seeing if it can be implemented into the program to increase search efficiency?
- RAG will not increase efficiency since the queries we handle are only the fault codes. Not any user inputs which may be very unclear eg: "car is not starting"
- for real time monitoring, viewing CAN (Controller area network of the car). it broadcasts codes and information to every ecu instead of a "from to" system. Its meant to be very reliable and engineers love it seems.
- How do you extract CAN data in real time from the ecu. Look into how F1 has a real time monitoring, maybe cars work the same way..
