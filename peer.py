import cv2
import socket
import numpy as np

def start_client(server_ip='localhost', port=9999, buffer_size=65536):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send a handshake message to the server
    handshake_message = "READY"
    client_socket.sendto(handshake_message.encode(), (server_ip, port))
    print(f"Sent handshake message to server at {server_ip}:{port}")

    data_buffer = b''  # Buffer to store incoming chunks

    while True:
        try:
            # Receive data chunks
            chunk, _ = client_socket.recvfrom(buffer_size)
            if not chunk:
                break

            # Append chunk to the buffer
            data_buffer += chunk

            # Check for end-of-frame marker
            if len(chunk) < buffer_size:  # Assuming the last chunk of a frame is smaller
                # Convert bytes to numpy array
                frame = np.frombuffer(data_buffer, dtype=np.uint8)
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                # Display the frame
                if frame is not None:
                    cv2.imshow('Client - Streaming', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                # Clear the buffer for the next frame
                data_buffer = b''
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()
    cv2.destroyAllWindows()

start_client('localhost', 9999)