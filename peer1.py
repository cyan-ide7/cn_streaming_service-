import cv2
import socket
import numpy as np

def start_client(server_ip='host', port=8888, buffer_size=65000):
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

            # Check for end-of-frame marker
            # Check for end-of-frame marker
            if chunk == b'END':
                if len(data_buffer) == 0:
                    print("Warning: Received END but data_buffer is empty.")
                    continue

                # Convert bytes to numpy array
                frame_data = np.frombuffer(data_buffer, dtype=np.uint8)
                frame = cv2.imdecode(frame_data, cv2.IMREAD_COLOR)

                if frame is None:
                    print("Warning: Failed to decode frame.")
                else:
                    cv2.imshow('Client - Streaming', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                data_buffer = b''  # Reset buffer

            else:
                # Append chunk to the buffer
                data_buffer += chunk
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()
    cv2.destroyAllWindows()

start_client('host', 8888)
