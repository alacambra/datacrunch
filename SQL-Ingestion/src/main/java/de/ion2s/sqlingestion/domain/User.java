package de.ion2s.sqlingestion.domain;

import java.util.Collection;

import org.neo4j.graphdb.Direction;
import org.springframework.data.neo4j.annotation.GraphId;
import org.springframework.data.neo4j.annotation.NodeEntity;
import org.springframework.data.neo4j.annotation.RelatedTo;

@NodeEntity
public class User {

	@GraphId
	private Long id;
	
	private String name;
	
	@RelatedTo(type="knows", direction = Direction.OUTGOING)
	private Collection<User> friends;
	
}
