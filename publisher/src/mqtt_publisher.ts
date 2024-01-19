import {mqtt, iot} from 'aws-iot-device-sdk-v2';

interface SwitchBotTopicBody {
    location: string,
    switch_name: string,
    state: boolean
}

interface MqttPublisher {
    publish(topic: string, body: SwitchBotTopicBody): Promise<void>
}

class MqttPublisherImpl implements MqttPublisher {
    private mqttClientConnection: mqtt.MqttClientConnection
    constructor() {
        if(typeof(process.env.AWS_IOT_ENDPOINT)==="undefined") {
            throw new Error("Environment variable: AWS_IOT_ENDPOINT is not defnied");
        }
        const client = new mqtt.MqttClient();
        const builder = iot.AwsIotMqttConnectionConfigBuilder.new_mtls_builder_from_path("./cert/certificate.pem.crt","./cert/private.pem.key");
        builder.with_client_id("switchbot-publisher");
        builder.with_certificate_authority_from_path(undefined,"./cert/AmazonRootCA1.pem");
        builder.with_endpoint(process.env.AWS_IOT_ENDPOINT);
        this.mqttClientConnection = client.new_connection(builder.build());
    }
    async publish(topic: string, body: SwitchBotTopicBody) {
        try {
            console.log("tls negotiation...");
            await this.mqttClientConnection.connect();
            console.log("connected");
            console.log(`publish message -> topic: ${topic}, message: ${JSON.stringify(body)}`);
            await this.mqttClientConnection.publish(topic, JSON.stringify(body),mqtt.QoS.AtLeastOnce);
            console.log("publish complete");
            await this.mqttClientConnection.disconnect();
            console.log("connection closed");
        } catch(error: any) {
            console.error(error);
        }
    }
}

export const MqttPublisher = {
    build: (): MqttPublisher=> {
        return new MqttPublisherImpl();
    }
}
