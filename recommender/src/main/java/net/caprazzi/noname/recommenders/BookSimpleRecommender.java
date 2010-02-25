package net.caprazzi.noname.recommenders;

import java.io.File;
import java.io.IOException;
import java.util.List;

import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.impl.common.FastByIDMap;
import org.apache.mahout.cf.taste.impl.common.FastIDSet;
import org.apache.mahout.cf.taste.impl.model.GenericBooleanPrefDataModel;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.neighborhood.NearestNUserNeighborhood;
import org.apache.mahout.cf.taste.impl.recommender.GenericBooleanPrefUserBasedRecommender;
import org.apache.mahout.cf.taste.impl.similarity.TanimotoCoefficientSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.neighborhood.UserNeighborhood;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;
import org.apache.mahout.cf.taste.recommender.Recommender;
import org.apache.mahout.cf.taste.similarity.UserSimilarity;

public class BookSimpleRecommender {

	public Recommender buildBooleanRecommender(FastByIDMap<FastIDSet> userData) {
		GenericBooleanPrefDataModel model = new GenericBooleanPrefDataModel(userData);
		UserSimilarity similarity = new TanimotoCoefficientSimilarity(model);
		UserNeighborhood neighborhood = new NearestNUserNeighborhood(10, similarity, model);
		Recommender recommender = new GenericBooleanPrefUserBasedRecommender(model, neighborhood, similarity);
		return recommender;
	}
	
	public static void main(String[] args) {
		DataModel model;
		try {
			model = new GenericBooleanPrefDataModel(new FileDataModel(new File("/Users/dikappa/Documents/workspace/rt-pub/my_items_cluster/data.txt")));
			UserSimilarity similarity = new TanimotoCoefficientSimilarity(model);
			UserNeighborhood neighborhood = new NearestNUserNeighborhood(10, similarity, model);
			Recommender recommender = new GenericBooleanPrefUserBasedRecommender(model, neighborhood, similarity);
			List<RecommendedItem> recommendations = recommender.recommend(1768, 3);
			for (RecommendedItem recommendation: recommendations){
				System.out.println(recommendation);
			}
		} catch (TasteException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
