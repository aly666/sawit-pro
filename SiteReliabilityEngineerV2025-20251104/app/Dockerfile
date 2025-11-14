# This is the Dockerfile for the application.
# You may need to modify this file to install the necessary packages, environment variables, etc.
FROM ubuntu:latest

# Set working directory
WORKDIR /app

# Copy the compiled Go binary from the build context
#COPY app-linux-amd64 app
COPY app-linux-amd64 ./app

# Make sure the binary is executable (in case it's not)
RUN chmod +x ./app

# Set entrypoint to run the app
CMD ["./app"]
