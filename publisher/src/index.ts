import { getIntentName, getRequestType, HandlerInput, SkillBuilders } from 'ask-sdk-core';
import {Response} from 'ask-sdk-model';
import {MqttPublisher} from './mqtt_publisher';

const TOPIC_ID = "switchbot";
const SWITCH_NAME = "kitchen1";
const LOCATION = "kitchen";

const SwitchOffIntentHandler = {
    canHandle(handlerInput: HandlerInput) {
        return getRequestType(handlerInput.requestEnvelope) === 'IntentRequest' &&
            getIntentName(handlerInput.requestEnvelope) === 'SwitchOnIntent';
    },
    async handle(handlerInput: HandlerInput) {
        const publisher = MqttPublisher.build();
        await publisher.publish(TOPIC_ID,{location: LOCATION, switch_name: SWITCH_NAME, state: true});
        return handlerInput.responseBuilder.speak("").getResponse();
    }
}
const SwitchOnIntentHandler = {
    canHandle(handlerInput: HandlerInput) {
        return getRequestType(handlerInput.requestEnvelope) === 'IntentRequest' &&
            getIntentName(handlerInput.requestEnvelope) === 'SwitchOffIntent';
    },
    async handle(handlerInput: HandlerInput) {
        const publisher = MqttPublisher.build();
        await publisher.publish(TOPIC_ID,{location: LOCATION, switch_name: SWITCH_NAME, state: false});
        return handlerInput.responseBuilder.speak("").getResponse();
    }
}

const SessionEndedRequestHandler = {
    canHandle(handlerInput: HandlerInput) {
        return getRequestType(handlerInput.requestEnvelope) === 'SessionEndedRequest';
    },
    handle(handlerInput: HandlerInput) {
        return handlerInput.responseBuilder.getResponse();
    }
};
const LaunchRequestHandler = {
    canHandle(handlerInput: HandlerInput) {
        return getRequestType(handlerInput.requestEnvelope) === 'LaunchRequest';
    },
    handle(handlerInput: HandlerInput) {
        const speakOutput = `電気を点ける、または消すを指定してください。`;

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .getResponse();
    }
};

const ErrorHandler = {
    canHandle() {
        return true;
    },
    handle(handlerInput: HandlerInput, error: Error) {
        console.error(`Error handled: ${error.message}`);
        console.error(`Error stack`, JSON.stringify(error.stack));
        console.error(`Error`, JSON.stringify(error));

        const speakOutput = 'エラーが発生しました';

        return handlerInput.responseBuilder
            .speak(speakOutput)
            .reprompt(speakOutput)
            .getResponse();
    }
};

const LogRequestInterceptor = {
    process(handlerInput: HandlerInput) {
        console.log(`RESPONSE=${JSON.stringify(handlerInput.requestEnvelope)}`);
    }
}

const LogResponseInterceptor = {
    process(handlerInput: HandlerInput, response: Response) {
        console.log(`RESPONSE=${JSON.stringify(response)}`);
    }
}

exports.handler = SkillBuilders.custom().addRequestHandlers(SessionEndedRequestHandler, LaunchRequestHandler, SwitchOnIntentHandler, SwitchOffIntentHandler).addErrorHandlers(ErrorHandler).addRequestInterceptors(LogRequestInterceptor).addResponseInterceptors(LogResponseInterceptor).lambda();