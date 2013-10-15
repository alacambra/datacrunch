package de.ion2s.sqlingestion.repo;

import org.springframework.data.neo4j.repository.GraphRepository;

import de.ion2s.sqlingestion.domain.User;

public interface UserRepository extends GraphRepository<User> {

}
