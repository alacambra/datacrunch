package poolingpeople.datacrunch.redmine;

// Generated Oct 28, 2013 5:31:36 PM by Hibernate Tools 4.0.0

import javax.persistence.Column;
import javax.persistence.Embeddable;

/**
 * ActivitiesByIssueId generated by hbm2java
 */
@Embeddable
public class ActivitiesByIssueId implements java.io.Serializable {

	private int issueId;
	private Integer parentId;
	private String activity;
	private Double investedTime;
	private String subject;

	public ActivitiesByIssueId() {
	}

	public ActivitiesByIssueId(int issueId, String activity, String subject) {
		this.issueId = issueId;
		this.activity = activity;
		this.subject = subject;
	}

	public ActivitiesByIssueId(int issueId, Integer parentId, String activity,
			Double investedTime, String subject) {
		this.issueId = issueId;
		this.parentId = parentId;
		this.activity = activity;
		this.investedTime = investedTime;
		this.subject = subject;
	}

	@Column(name = "issue_id", nullable = false)
	public int getIssueId() {
		return this.issueId;
	}

	public void setIssueId(int issueId) {
		this.issueId = issueId;
	}

	@Column(name = "parent_id")
	public Integer getParentId() {
		return this.parentId;
	}

	public void setParentId(Integer parentId) {
		this.parentId = parentId;
	}

	@Column(name = "activity", nullable = false, length = 30)
	public String getActivity() {
		return this.activity;
	}

	public void setActivity(String activity) {
		this.activity = activity;
	}

	@Column(name = "invested_time", precision = 22, scale = 0)
	public Double getInvestedTime() {
		return this.investedTime;
	}

	public void setInvestedTime(Double investedTime) {
		this.investedTime = investedTime;
	}

	@Column(name = "subject", nullable = false)
	public String getSubject() {
		return this.subject;
	}

	public void setSubject(String subject) {
		this.subject = subject;
	}

	public boolean equals(Object other) {
		if ((this == other))
			return true;
		if ((other == null))
			return false;
		if (!(other instanceof ActivitiesByIssueId))
			return false;
		ActivitiesByIssueId castOther = (ActivitiesByIssueId) other;

		return (this.getIssueId() == castOther.getIssueId())
				&& ((this.getParentId() == castOther.getParentId()) || (this
						.getParentId() != null
						&& castOther.getParentId() != null && this
						.getParentId().equals(castOther.getParentId())))
				&& ((this.getActivity() == castOther.getActivity()) || (this
						.getActivity() != null
						&& castOther.getActivity() != null && this
						.getActivity().equals(castOther.getActivity())))
				&& ((this.getInvestedTime() == castOther.getInvestedTime()) || (this
						.getInvestedTime() != null
						&& castOther.getInvestedTime() != null && this
						.getInvestedTime().equals(castOther.getInvestedTime())))
				&& ((this.getSubject() == castOther.getSubject()) || (this
						.getSubject() != null && castOther.getSubject() != null && this
						.getSubject().equals(castOther.getSubject())));
	}

	public int hashCode() {
		int result = 17;

		result = 37 * result + this.getIssueId();
		result = 37 * result
				+ (getParentId() == null ? 0 : this.getParentId().hashCode());
		result = 37 * result
				+ (getActivity() == null ? 0 : this.getActivity().hashCode());
		result = 37
				* result
				+ (getInvestedTime() == null ? 0 : this.getInvestedTime()
						.hashCode());
		result = 37 * result
				+ (getSubject() == null ? 0 : this.getSubject().hashCode());
		return result;
	}

}
