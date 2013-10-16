package poolingpeople.datacrunch;

import java.util.List;

public interface IIngestorFactory {

	public abstract List<IBasicInfoView> getAllEntries();

}