package poolingpeople.datacrunch;

import java.util.List;

import org.hibernate.Session;

public class IngestorFactory implements IIngestorFactory  {

	
//	public static void main(String[] args){
//		List<IBasicInfoView> bl = getAllEntries();
//
//		for (IBasicInfoView b : bl) {
//			System.out.println(b.getIssue_description());
//		}
//	}
	
	@Override
	public List<IBasicInfoView> getAllEntries(){

		Session s = HibernateUtil.getSessionFactory().getCurrentSession();
		s.beginTransaction();
		List<IBasicInfoView> bl = (List<IBasicInfoView>) s.getNamedQuery("getAll").list();
		s.getTransaction().commit();

		return bl;
	}
	
	public static void main(String[] args) {
		
		Session s = HibernateUtil.getSessionFactory().getCurrentSession();
		s.beginTransaction();
		Object a = s.getNamedQuery("getAllUsers").list();
		s.getTransaction().commit();
	}
}











































