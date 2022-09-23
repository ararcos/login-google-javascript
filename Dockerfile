#Add tag of docker_base
FROM 388813176377.dkr.ecr.us-east-1.amazonaws.com/office_desk_reservations_base:base_project

# Copy function code to container
COPY ./desk_reservation/bookings/infrastructure/controllers/create_booking.py ./

# setting the CMD
CMD ["create_booking.create_book"]
