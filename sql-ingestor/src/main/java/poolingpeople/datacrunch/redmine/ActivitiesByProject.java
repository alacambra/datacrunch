package poolingpeople.datacrunch.redmine;

// Generated Oct 28, 2013 5:31:36 PM by Hibernate Tools 4.0.0

import javax.persistence.AttributeOverride;
import javax.persistence.AttributeOverrides;
import javax.persistence.Column;
import javax.persistence.EmbeddedId;
import javax.persistence.Entity;
import javax.persistence.Table;

/**
 * ActivitiesByProject generated by hbm2java
 */
@Entity
@Table(name = "activities_by_project", catalog = "redmine")
public class ActivitiesByProject implements java.io.Serializable {

	private ActivitiesByProjectId id;

	public ActivitiesByProject() {
	}

	public ActivitiesByProject(ActivitiesByProjectId id) {
		this.id = id;
	}

	@EmbeddedId
	@AttributeOverrides({
			@AttributeOverride(name = "projectId", column = @Column(name = "project_id", nullable = false)),
			@AttributeOverride(name = "parentId", column = @Column(name = "parent_id")),
			@AttributeOverride(name = "activity", column = @Column(name = "activity", nullable = false, length = 30)),
			@AttributeOverride(name = "investedTime", column = @Column(name = "invested_time", precision = 22, scale = 0)),
			@AttributeOverride(name = "projectName", column = @Column(name = "project_name", nullable = false)),
			@AttributeOverride(name = "projectDescription", column = @Column(name = "project_description", length = 65535)) })
	public ActivitiesByProjectId getId() {
		return this.id;
	}

	public void setId(ActivitiesByProjectId id) {
		this.id = id;
	}

}