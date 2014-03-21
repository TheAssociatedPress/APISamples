package ap.apisample;

import java.net.URL;
import java.net.URLEncoder;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;
import org.w3c.dom.Document;

/**
 *
 * @author Prasad Bapatla
 */
public class APIClient {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {

        try {
            // sign up for developer key at http://developer.ap.org/
            String apikey = "";
            String keyword_search = "obama";
            
            // build url
            String url = "http://api.ap.org/v2/search?count=1&apikey=" + apikey + "&q=" + URLEncoder.encode(keyword_search,"UTF-8");
            
            //
            DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
            DocumentBuilder db = dbf.newDocumentBuilder();
            
            // fetch the response from url
            Document doc = (Document) db.parse(new URL(url).openStream());

            // transform the xml response
            TransformerFactory transformerFactory = TransformerFactory.newInstance();
                        
            Transformer xform = transformerFactory.newTransformer();
            xform.setOutputProperty(OutputKeys.INDENT, "yes");  // indent for easy read
            xform.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "4");
            xform.transform(new DOMSource(doc), new StreamResult(System.out));
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }
    }
}
