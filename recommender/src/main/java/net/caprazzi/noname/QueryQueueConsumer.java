package net.caprazzi.noname;

import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.DefaultConsumer;
import com.rabbitmq.client.Envelope;
import com.rabbitmq.client.AMQP.BasicProperties;

public class QueryQueueConsumer extends DefaultConsumer {
	
	Logger logger = LoggerFactory.getLogger(QueryQueueConsumer.class);
	private QueryResolverService queryResolverService;
	
	public QueryQueueConsumer(Channel channel) {
		super(channel);
	}
	
	@Override
	public void handleDelivery(String consumerTag, Envelope envelope,
			BasicProperties properties, byte[] body) throws IOException {
		String routingKey = envelope.getRoutingKey();
        String contentType = properties.getContentType();
        long deliveryTag = envelope.getDeliveryTag();
        // (process the message components ...)
        String messageId = "messageId";
        String[] query = new String[1];
        
        // if the resolver service accepts the job, remove the message from the queue
        // the resolver will take care of putting a response on the queue
        if (queryResolverService.resolve(messageId, query)) {
        	getChannel().basicAck(deliveryTag, false);
        }
	}

	public void setQueryResolverService(QueryResolverService queryResolverService) {
		this.queryResolverService = queryResolverService;
	}
	
	

}
