package poolingpeople.datacrunch;

import java.lang.reflect.Field;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.List;


import org.hibernate.Criteria;
import org.hibernate.Session;
import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Node;
import org.neo4j.graphdb.Relationship;
import org.neo4j.graphdb.RelationshipType;
import org.neo4j.graphdb.Transaction;
import org.neo4j.graphdb.factory.GraphDatabaseFactory;
//import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.index.IndexHits;
import org.neo4j.kernel.EmbeddedGraphDatabase;

import poolingpeople.datacrunch.redmine.Enumerations;
import poolingpeople.datacrunch.redmine.IsRedmineEntity;
import poolingpeople.datacrunch.redmine.Issues;
import poolingpeople.datacrunch.redmine.TimeEntries;
import poolingpeople.datacrunch.redmine.Users;

public class FromSqlToNeo4jIngestor {

	static GraphDatabaseService graphDb = new GraphDatabaseFactory().newEmbeddedDatabase( "target/neo4j-all" );
//	static GraphDatabaseService graphDb = new EmbeddedGraphDatabase("target/neo4j-all");
	
	public static void main(String[] args) {
		System.out.println("starting...");

		Transaction tx = graphDb.beginTx();
		try {
			FromSqlToNeo4jIngestor ingestor = new FromSqlToNeo4jIngestor();
			ingestNodes();
			System.out.println("Issues hierarchy");
			ingestor.buildIssuerHierarchy();
			System.out.println("Time entries hierarchies");
			ingestor.buildTimeEntries();
			tx.success();
		} catch (Exception e) {
			tx.failure();
			throw new RuntimeException(e);
		} finally {
			tx.finish();
			graphDb.shutdown();
			System.out.println("finished");
		}
		//		test();

	}

	public static void ingestNodes() {
		FromSqlToNeo4jIngestor ingestor = new FromSqlToNeo4jIngestor();
		System.out.println("Loading redmine entities");
		Session session = HibernateUtil.getSessionFactory().getCurrentSession();
		session.beginTransaction();
		Criteria criteria = session.createCriteria(Users.class);
		List<Users> users = criteria.list();

		criteria = session.createCriteria(TimeEntries.class);
		List<TimeEntries> timeEntries = criteria.list();

		criteria = session.createCriteria(Issues.class);
		List<Issues> issues = criteria.list();

		criteria = session.createCriteria(Enumerations.class);
		List<Enumerations> enumerations = criteria.list();

		session.getTransaction().commit();

		System.out.println("importing to neo");

		System.out.println("users");
		for(Users u : users) {
			ingestor.convert(u);
		}

		System.out.println("issues");
		for(Issues i : issues) {
			ingestor.convert(i);
		}

		System.out.println("services");
		for(Enumerations e : enumerations) {
			Node node = graphDb.createNode();
			String uid = e.getName();
			if(ingestor.nodeExists(uid)) continue;
			node.setProperty("uid", uid);
			graphDb.index().forNodes("entities").add(node, "type", "service");
			graphDb.index().forNodes("entities").add(node, "uid", uid);
		}

		System.out.println("Te's");
		for(TimeEntries te : timeEntries) {
			ingestor.convert(te);
		}

		ingestor.loadDatesNodes();
		System.out.println("succes");
	}

	private void loadDatesNodes() {
		for(int i = 2009; i<2015; i++) {
			Node node = graphDb.createNode();
			String uid = "year_" + i;
			node.setProperty("uid", uid);
			graphDb.index().forNodes("entities").add(node, "type", "year");
			graphDb.index().forNodes("entities").add(node, "uid", uid);
		}

		for(int i = 1; i<32; i++) {
			Node node = graphDb.createNode();
			String uid = "day_" + i;
			node.setProperty("uid", uid);
			graphDb.index().forNodes("entities").add(node, "type", "day");
			graphDb.index().forNodes("entities").add(node, "uid", uid);
		}

		for(int i = 1; i<32; i++) {
			Node node = graphDb.createNode();
			String uid = "month_" + i;
			node.setProperty("uid", uid);
			graphDb.index().forNodes("entities").add(node, "type", "month");
			graphDb.index().forNodes("entities").add(node, "uid", uid);
		}		
	}

	public static void test() {

		Transaction tx = graphDb.beginTx();
		try {
			IndexHits<Node> nHits = graphDb.index().forNodes("entities").get("type", Users.class.getSimpleName().toLowerCase());

			for( Node n : nHits ) {
				System.out.println(n.getProperty("uid"));
			}

			tx.success();
		} catch (Exception e) {
			tx.failure();
		} finally {
			tx.finish();
			graphDb.shutdown();
		}
	}

	public void convert(IsRedmineEntity entity) {
		String type = entity.getClass().getSimpleName().toLowerCase();
		Integer entityId = entity.getId();
		String uid = generateUUid(type, entityId);

		if(nodeExists(uid)) return;

		Node node = graphDb.createNode();
		node.setProperty("uid", uid);
		graphDb.index().forNodes("entities").add(node, "type", type);
		graphDb.index().forNodes("entities").add(node, "uid", uid);

		Field[] fields = entity.getClass().getDeclaredFields();

		for (int i = 0; i < fields.length; i++) {
			try {
				Object value = fields[i].get(entity);
				if (value != null) {
					node.setProperty(fields[i].getName(), value.toString());
				}
			} catch (Exception e) {
				System.err.println(e.getMessage());
				System.err.println(e);
			}
		}
	}

	public void buildIssuerHierarchy() {
		IndexHits<Node> nHits = graphDb.index().forNodes("entities").get("type", "issues");
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss.SSS");

		for(Node child : nHits) {
			if (child.hasProperty("parentId")) {
				String uid = generateUUid(
						Issues.class.getSimpleName().toLowerCase(), Integer.parseInt((String) child.getProperty("parentId")));

				Node parent = loadNode(uid);
				parent.createRelationshipTo(child, new RelationshipType(){
					public String name(){
						return "parent";
					};
				});
			}

			if (child.hasProperty("authorId")) {
				String uid = generateUUid(
						Users.class.getSimpleName().toLowerCase(), Integer.parseInt((String) child.getProperty("authorId")));

				Node user = loadNode(uid);
				user.createRelationshipTo(child, new RelationshipType(){
					public String name(){
						return "creates";
					};
				});
			}

			if (child.hasProperty("createdOn")) {

				String date = (String) child.getProperty("createdOn");

				try {
					Date d = sdf.parse(date);
					Calendar cal = Calendar.getInstance();
					cal.setTime(d);
					int day = cal.get(Calendar.DAY_OF_MONTH);
					int month = cal.get(Calendar.MONTH) + 1;
					int year = cal.get(Calendar.YEAR);

					Node dayNode = loadNode("day_" + day);
					Node monthNode = loadNode("month_" + month);
					Node yearNode = loadNode("year_" + year);

					RelationshipType rel = new RelationshipType(){
						public String name(){
							return "created_on";
						};
					};
					try {
						child.createRelationshipTo(dayNode, rel);
						child.createRelationshipTo(monthNode, rel);
						child.createRelationshipTo(yearNode, rel);
					} catch (IllegalArgumentException e) {
						throw e;
					}

				} catch (ParseException e) {
					e.printStackTrace();
				}

			}
		}
	}

	public void buildTimeEntries() {

		Session session = HibernateUtil.getSessionFactory().getCurrentSession();
		session.beginTransaction();
		Criteria criteria = session.createCriteria(Enumerations.class);
		List<Enumerations> enumerations = criteria.list();
		session.getTransaction().commit();
		HashMap<Integer, String> services = new HashMap<Integer, String>();
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");

		for(Enumerations enumeration : enumerations) {
			services.put(enumeration.getId(), enumeration.getName());
		}

		IndexHits<Node> nHits = graphDb.index().forNodes("entities").get("type", "timeentries");
		for(Node te : nHits) {
			if (te.hasProperty("issueId")) {
				String uid = generateUUid(
						Issues.class.getSimpleName().toLowerCase(), Integer.parseInt((String) te.getProperty("issueId")));

				Node issue = loadNode(uid);
				issue.createRelationshipTo(te, new RelationshipType(){
					public String name(){
						return "has_te";
					};
				});
			}

			if (te.hasProperty("userId")) {
				String uid = generateUUid(
						Users.class.getSimpleName().toLowerCase(), Integer.parseInt((String) te.getProperty("userId")));

				Node user = loadNode(uid);
				user.createRelationshipTo(te, new RelationshipType(){
					public String name(){
						return "books";
					};
				});
			}

			if (te.hasProperty("activityId")) {

				String uid = services.get(Integer.parseInt((String) te.getProperty("activityId")));

				Node service = loadNode(uid);
				te.createRelationshipTo(service, new RelationshipType(){
					public String name(){
						return "service";
					};
				}).setProperty("hours", Float.parseFloat((String) te.getProperty("hours")));

			}

			if (te.hasProperty("spentOn")) {

				String date = (String) te.getProperty("spentOn");

				try {
					Date d = sdf.parse(date);
					Calendar cal = Calendar.getInstance();
					cal.setTime(d);
					int day = cal.get(Calendar.DAY_OF_MONTH);
					int month = cal.get(Calendar.MONTH) + 1;
					int year = cal.get(Calendar.YEAR);

					Node dayNode = loadNode("day_" + day);
					Node monthNode = loadNode("month_" + month);
					Node yearNode = loadNode("year_" + year);

					RelationshipType rel = new RelationshipType(){
						public String name(){
							return "spent_on";
						};
					};
					
					try {
						te.createRelationshipTo(dayNode, rel);
						te.createRelationshipTo(monthNode, rel);
						te.createRelationshipTo(yearNode, rel);
					} catch (IllegalArgumentException e) {
						throw e;
					}

				} catch (ParseException e) {
					e.printStackTrace();
				}

			}
		}
	}

	public Node loadNode(String uid) {
		return graphDb.index().forNodes("entities").get("uid", uid).getSingle();
	}

	public boolean nodeExists(String uid) {
		return graphDb.index().forNodes("entities").get("uid", uid).size() > 0;
	}

	public String generateUUid(String type, Integer id) {

		return type + "_" + String.valueOf(id);

	}

}














































