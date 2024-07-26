# Veterinary Finder

This project is a Minimum Viable Product (MVP) web application designed to help users find veterinary clinics based on various filters. The application is built using Python with Streamlit for the user interface and Pydeck for map visualization. It uses geocoding to map the locations of veterinary clinics. This MVP will be improved to enhance usability for my local community.

## Features

- **Filter**: Apply filters to find clinics that meet specific criteria, such as emergency services, special rates for rescued animals, and home service.
- **Map Visualization**: View veterinary clinics on an interactive map with detailed information on each clinic.

## Installation

To set up the project on your local machine, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/cvillarragamo/Vet_Mexicali.git


## Code Overview

- **fetch_veterinarias()**: Loads the data from the Excel file.
- **geocode_address(address, geolocator)**: Geocodes the address to retrieve latitude and longitude.
- **Streamlit UI**: Provides options to filter and display veterinary clinics on a map using Pydeck.
