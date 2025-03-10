import asyncio
import random
from asyncua import ua, Server

async def main():
    # Initialize the OPC UA server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://localhost:4840/")

    # Register a new namespace for the server
    uri = "http://example.uri.randomdata"
    idx = await server.register_namespace(uri)

    # Create a folder in the server's address space
    objects_node = server.nodes.objects
    random_data_folder = await objects_node.add_folder(idx, "RandomDataGenerator")

    # Create variables within the RandomDataGenerator folder with explicit types
    temperature_var = await random_data_folder.add_variable(
        idx, "Temperature", 0.0, ua.VariantType.Double)
    pressure_var = await random_data_folder.add_variable(
        idx, "Pressure", 0.0, ua.VariantType.Double)
    humidity_var = await random_data_folder.add_variable(
        idx, "Humidity", 0.0, ua.VariantType.Double)

    # Set the variables to be writable
    await temperature_var.set_writable()
    await pressure_var.set_writable()
    await humidity_var.set_writable()

    # Start the server
    await server.start()
    print("OPC UA Server started at opc.tcp://localhost:4840/freeopcua/server/")

    try:
        # Infinite loop to update variables with random data
        while True:
            # Generate random values
            temperature = round(random.uniform(20.0, 30.0), 2)
            pressure = round(random.uniform(1.0, 2.0), 2)
            humidity = round(random.uniform(30.0, 70.0), 2)

            # Update the variables on the server
            await temperature_var.write_value(temperature)
            await pressure_var.write_value(pressure)
            await humidity_var.write_value(humidity)

            # Print the updated values for debugging
            print(f"Updated Temperature: {temperature} °C, Pressure: {pressure} bar, Humidity: {humidity} %")

            # Wait 1 second before the next update
            await asyncio.sleep(1)
    finally:
        # Stop the server when exiting
        await server.stop()
        print("Server stopped")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())