import spacy, sklearn_crfsuite
from .base import BasePipeline
from ..pipeline_components import ClinicalTokenizer
from ..learn.feature_extractor import FeatureExtractor

from ..pipeline_components import GoldAnnotatorComponent, MetaMapComponent, UnitComponent


class ClinicalPipeline(BasePipeline):
    """
    A pipeline for clinical named entity recognition
    """

    def __init__(self, metamap, entities=[]):
        """
        Create a pipeline with the name 'clinical_pipeline' utilizing
        by default spaCy's small english model.

        :param metamap: an instance of MetaMap
        """
        super().__init__("clinical_pipeline", spacy.load("en_core_web_sm"))


        self.spacy_pipeline.tokenizer = self.get_tokenizer() #set tokenizer

        self.add_component(GoldAnnotatorComponent, entities) #add overlay for GoldAnnotation
        self.add_component(MetaMapComponent, metamap)
        self.add_component(UnitComponent)

    def __call__(self, doc):
        """
        Passes a single document through the pipeline.
        All relevant document attributes should be set prior to this call.
        :param self:
        :param doc:
        :return:
        """

        for component_name, proc in self.spacy_pipeline.pipeline:
            doc = proc(doc)
            if component_name == 'ner':
                # remove labeled default entities
                doc.ents = []

        return doc
            


    def get_learner(self):
        return sklearn_crfsuite.CRF(
            algorithm='lbfgs',
            max_iterations=100,
            all_possible_transitions=True
        )

    def get_tokenizer(self):
        tokenizer = ClinicalTokenizer(self.spacy_pipeline)
        return tokenizer.tokenizer

    def get_feature_extractor(self):
        extractor = FeatureExtractor(window_size = 2, spacy_features=['pos_', 'shape_', 'prefix_', 'suffix_', 'like_num'])
        return extractor







