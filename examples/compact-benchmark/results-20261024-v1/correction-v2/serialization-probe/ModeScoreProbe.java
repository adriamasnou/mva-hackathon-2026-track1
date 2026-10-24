import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.annotation.JsonInclude;
import org.monarchinitiative.exomiser.core.model.GeneScore;

public class ModeScoreProbe {
  public static void main(String[] args) throws Exception {
    ObjectMapper mapper = new ObjectMapper();
    mapper.addMixIn(Class.forName("org.monarchinitiative.exomiser.core.model.Gene"),
      Class.forName("org.monarchinitiative.exomiser.core.writers.JsonGeneMixin"));
    mapper.addMixIn(Class.forName("org.monarchinitiative.svart.GenomicVariant"),
      Class.forName("org.monarchinitiative.exomiser.core.writers.JsonVariantMixin"));
    mapper.setDefaultPropertyInclusion(JsonInclude.Include.NON_DEFAULT);
    GeneScore zero = GeneScore.empty();
    GeneScore positive = GeneScore.builder().combinedScore(0.125).build();
    String zeroJSON = mapper.writeValueAsString(zero);
    String positiveJSON = mapper.writeValueAsString(positive);
    if (zero.combinedScore() != 0.0 || mapper.readTree(zeroJSON).has("combinedScore"))
      throw new IllegalStateException("Default-zero suppression did not reproduce");
    if (mapper.readTree(positiveJSON).get("combinedScore").asDouble() != 0.125)
      throw new IllegalStateException("Nonzero score serialization did not reproduce");
    System.out.println("zero_numeric=" + zero.combinedScore());
    System.out.println("zero_json=" + zeroJSON);
    System.out.println("positive_json=" + positiveJSON);
    System.out.println("PASS: installed GeneScore plus writer ObjectMapper configuration suppresses zero and retains nonzero");
  }
}
