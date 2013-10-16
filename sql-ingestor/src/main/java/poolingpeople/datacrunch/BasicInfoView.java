package poolingpeople.datacrunch;

import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.NamedQueries;
import javax.persistence.NamedQuery;

import org.hibernate.annotations.Type;

@NamedQueries(
		value = { 
				@NamedQuery(name = "getAll", query = "from basic_info") 
			})

@Entity(name="basic_info")
public class BasicInfoView implements IBasicInfoView {

	@Id
	private int id;
	private String tracker;
	private String activity;
	private String project_name;
	private String issue_subject;
	@Type(type = "text")
	private String issue_description;
	private String te_comments;
	private String firstname;

	public BasicInfoView() {
		super();
	}

	@Override
	public String getTracker() {
		return tracker;
	}
	@Override
	public String getActivity() {
		return activity;
	}
	@Override
	public String getProject_name() {
		return project_name;
	}
	@Override
	public String getIssue_subject() {
		return issue_subject;
	}
	@Override
	public String getIssue_description() {
		return issue_description;
	}
	@Override
	public String getTe_comments() {
		return te_comments;
	}
	@Override
	public String getFirstname() {
		return firstname;
	}

	public void setTracker(String tracker) {
		this.tracker = tracker;
	}

	public void setActivity(String activity) {
		this.activity = activity;
	}

	public void setProject_name(String project_name) {
		this.project_name = project_name;
	}

	public void setIssue_subject(String issue_subject) {
		this.issue_subject = issue_subject;
	}

	public void setIssue_description(String issue_description) {
		this.issue_description = issue_description;
	}

	public void setTe_comments(String te_comments) {
		this.te_comments = te_comments;
	}

	public void setFirstname(String firstname) {
		this.firstname = firstname;
	}
}
