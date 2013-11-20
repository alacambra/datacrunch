package poolingpeople.datacrunch;

import com.tinkerpop.blueprints.Graph;
import com.tinkerpop.blueprints.impls.neo4j.Neo4jGraph;


public class Neo4jExporter {
	public Neo4jExporter() {
		Graph g = new Neo4jGraph( "target/neo4j-all" );
		
	}
}
