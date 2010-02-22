package net.caprazzi.noname;

import java.io.IOException;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.ConnectionParameters;
import com.rabbitmq.client.Connection;

import com.rabbitmq.client.Consumer;
import com.rabbitmq.client.QueueingConsumer;
import com.rabbitmq.tools.json.JSONReader;

/**
 * reads query-queue
 * writes response-queue
 */
public class App {
	
    public static void main( String[] args ) throws IOException, JSONException {
    	
    	ConnectionParameters params = new ConnectionParameters();
    	params.setUsername("guest");
    	params.setPassword("guest");
    	params.setVirtualHost("/");
    	params.setRequestedHeartbeat(0);
    	ConnectionFactory factory = new ConnectionFactory(params);
    	Connection conn = factory.newConnection("localhost", 5672);
    	
    	// safety: never use a channel in different threads
    	Channel channel = conn.createChannel();
    	
    	channel.queueDeclare("query-queue");
    	channel.queueDeclare("response-queue");
    	channel.exchangeDeclare("response-exchange", "fanout");
    	channel.queueBind("response-queue", "response-exchange", "ugo");
    	
    	boolean noAck = false;
    	QueueingConsumer consumer = new QueueingConsumer(channel);
    	channel.basicConsume("query-queue", noAck, consumer);
    	System.out.println("ok");
    	while (true) {
    	    QueueingConsumer.Delivery delivery;
    	    System.out.println("out");
    	    try {
    	        delivery = consumer.nextDelivery();
    	        System.out.println(delivery);
    	    } catch (InterruptedException ie) {
    	    	System.out.println(ie.toString());
    	        continue;
    	    }
    	    // (process the message components ...)
    	    JSONObject jsonObject = new JSONObject(delivery.getBody());
    		String messageId = (String) jsonObject.get("message_id");
    		JSONObject body = (JSONObject) jsonObject.get("body");
    		JSONArray query = (JSONArray) body.get("web_query");
    		String[] profiles = new String[query.length()];
    		System.out.println("received message " + messageId);
    		for (String string : profiles) {
				System.out.println(profiles);
			}
    	    
    	    channel.basicAck(delivery.getEnvelope().getDeliveryTag(), false);
    	}
    	
    	
    }
}
