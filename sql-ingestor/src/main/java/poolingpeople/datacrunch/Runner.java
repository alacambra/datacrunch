package poolingpeople.datacrunch;

import java.util.List;

public class Runner {

	public static void main(String[] args) {
		
		IIngestorFactory factory = new IngestorFactory();
		
		List<IBasicInfoView> bl = factory.getAllEntries();

		for (IBasicInfoView b : bl) {
			System.out.println("-----------------------");
			System.out.println(b.getIssue_description());
		}
		
	}

}
