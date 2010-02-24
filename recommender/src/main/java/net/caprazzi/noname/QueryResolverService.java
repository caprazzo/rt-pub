package net.caprazzi.noname;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.RejectedExecutionException;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class QueryResolverService {
	Logger logger = LoggerFactory.getLogger(App.class);
	
	private ThreadPoolExecutor executor;
	private QueryResolverFactory queryResolverFactory;
	public QueryResolverService(int corePoolSize, int maximumPoolSize, int maxQueueSize) {
		// using a bound queue and finite pool sizes, new tasks
		// should be rejected when the queue is full
		ArrayBlockingQueue<Runnable> workQueue = new ArrayBlockingQueue<Runnable>(maxQueueSize);
		executor = new ThreadPoolExecutor(corePoolSize, maximumPoolSize, Long.MAX_VALUE, TimeUnit.NANOSECONDS, workQueue);
	}
	
	public void setQueryResolverFactory(QueryResolverFactory queryResolverFactory) {
		this.queryResolverFactory = queryResolverFactory;
	}
	
	public boolean resolve(final String messageId, final String[] query) {
		logger.info("Received request to resolve query {}: {}", messageId, query);
		final QueryResolver resolver = queryResolverFactory.createResolver();
		Runnable task = new Runnable() {			
			@Override public void run() {
				resolver.resolve(messageId, query);
			}
		};
		
		try {
			executor.execute(task);
			logger.info("Job accepted {}", messageId);
			return true;
		} 
		catch (RejectedExecutionException  e) {
			logger.warn("Job Rejected " + messageId, e);
			return false;
		}
		
	}

}
