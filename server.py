import cv2
import socket
import numpy as np
import time  # Import time module for adding delay

def start_stream(video_path, host='localhost', port=9999, chunk_size=65000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))

    print("Server is waiting for client to connect...")
    
    # Wait for a handshake message from the client
    handshake_message, client_address = server_socket.recvfrom(1024)
    print(f"Client connected from {client_address}: {handshake_message.decode()}")

    print("Server is streaming on {}:{}".format(host, port))
    
    while True:  # Loop to allow replaying the video
        cap = cv2.VideoCapture(video_path)
        frame_rate = cap.get(cv2.CAP_PROP_FPS)  # Get the frame rate of the video
        frame_delay = 1 / frame_rate if frame_rate > 0 else 0.03  # Calculate delay dynamically

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    print("Video ended.")
                    break
                
                # Compress and encode frame
                _, buffer = cv2.imencode('.jpg', frame)
                data = buffer.tobytes()
                
                # Split data into chunks and send
                for i in range(0, len(data), chunk_size):
                    chunk = data[i:i + chunk_size]
                    server_socket.sendto(chunk, client_address)
                
                # Send end-of-frame marker
                server_socket.sendto(b'END', client_address)

                # Add a delay to control the frame rate
                time.sleep(frame_delay)
        finally:
            cap.release()

        # Ask the user if they want to replay the video
        replay = input("Replay the video? (y/n): ").strip().lower()
        if replay != 'y':
            break

    server_socket.close()

start_stream('video.mp4')
