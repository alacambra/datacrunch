package poolingpeople.datacrunch;

import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

public class HibernateUtil {

	private static final SessionFactory sessionFactory = buildSessionFactory();
//	private static ServiceRegistry serviceRegistry;

	private static SessionFactory buildSessionFactory() {
		try {
			Configuration configuration = new Configuration();
			configuration.configure();
//			serviceRegistry = new ServiceRegistryBuilder().buildServiceRegistry();        

			return new Configuration().configure().buildSessionFactory();
		}
		catch (Throwable ex) {
			throw new ExceptionInInitializerError(ex);
		}
	}

	public static SessionFactory getSessionFactory() {
		return sessionFactory;
	}
}