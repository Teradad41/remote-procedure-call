import { Socket } from 'net';


const server_ip = '127.0.0.1';
const server_port = 12345;

const client = new Socket();

let id = 1;

const createRequest = (method, params, paramTypes) => ({
  "method": method,
  "params": params,
  "param_type": paramTypes,
  "id": id,
});

const sendRequest = (request) => {
  client.connect(server_port, server_ip, () => {
    console.log(`Connection to: ${server_ip}:${server_port}`);

    client.write(JSON.stringify(request))
    id++;
  })

  client.on('data', (data) => {
    console.log(`Response from server: ${data}`);
    client.end();
  });

  client.on('end', () => {
    console.log('Closing connection...');
  });
}

const request = createRequest("nroot", [3, 27], ["number", "number"], id);
sendRequest(request);
