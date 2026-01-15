"""Tests for the TermPredictor model."""
import pytest
from negotiation.models.predictor import TermPredictor


@pytest.fixture
def fitted_predictor():
    """Create a fitted predictor for testing."""
    predictor = TermPredictor(n_estimators=10, random_state=42)  # Fewer trees for speed
    predictor.fit('data/training/cuad.tsv')
    return predictor


class TestTermPredictor:
    """Tests for TermPredictor class."""

    def test_fit_loads_data(self, fitted_predictor):
        """Test that fit() loads and processes data correctly."""
        assert fitted_predictor._is_fitted
        assert fitted_predictor.data is not None
        assert len(fitted_predictor.data) > 400  # Should have ~500 rows after dropna
        assert len(fitted_predictor.models) == len(TermPredictor.TERM_COLUMNS)

    def test_predict_returns_all_unknown_terms(self, fitted_predictor):
        """Test that predict() returns predictions for all unknown terms."""
        known = {'Audit Rights': 1, 'Anti-Assignment': 0}
        results = fitted_predictor.predict(known)

        # Should return predictions for all terms except the known ones
        expected_count = len(TermPredictor.TERM_COLUMNS) - len(known)
        assert len(results) == expected_count

        # Should not include known terms in results
        assert 'Audit Rights' not in results
        assert 'Anti-Assignment' not in results

    def test_predict_returns_valid_format(self, fitted_predictor):
        """Test that predictions have correct format."""
        known = {'Cap On Liability': 1}
        results = fitted_predictor.predict(known)

        for term, pred in results.items():
            assert 'prediction' in pred
            assert 'probability' in pred
            assert pred['prediction'] in (0, 1)
            assert 0 <= pred['probability'] <= 1

    def test_predict_without_fit_raises(self):
        """Test that predict() raises error if model not fitted."""
        predictor = TermPredictor()
        with pytest.raises(RuntimeError, match="not fitted"):
            predictor.predict({'Audit Rights': 1})

    def test_evaluate_returns_scores(self, fitted_predictor):
        """Test that evaluate() returns accuracy scores for all terms."""
        results = fitted_predictor.evaluate(cv_folds=3)  # Fewer folds for speed

        assert len(results) == len(TermPredictor.TERM_COLUMNS)

        for term, scores in results.items():
            assert 'accuracy' in scores
            assert 'baseline' in scores
            assert 'lift' in scores
            assert 0 <= scores['accuracy'] <= 1
            assert 0 <= scores['baseline'] <= 1

    def test_feature_importance_returns_features(self, fitted_predictor):
        """Test that feature_importance() returns top features per term."""
        results = fitted_predictor.feature_importance()

        assert len(results) == len(TermPredictor.TERM_COLUMNS)

        for term, features in results.items():
            assert len(features) > 0
            assert len(features) <= 5  # Top 5
            for f in features:
                assert 'feature' in f
                assert 'importance' in f
                assert f['importance'] >= 0

    def test_predict_handles_single_known_term(self, fitted_predictor):
        """Test prediction with just one known term."""
        results = fitted_predictor.predict({'Audit Rights': 1})
        assert len(results) == len(TermPredictor.TERM_COLUMNS) - 1

    def test_predict_handles_many_known_terms(self, fitted_predictor):
        """Test prediction with many known terms."""
        known = {
            'Audit Rights': 1,
            'Anti-Assignment': 1,
            'Cap On Liability': 1,
            'Revenue/Profit Sharing': 0,
            'Termination For Convenience': 1,
        }
        results = fitted_predictor.predict(known)
        assert len(results) == len(TermPredictor.TERM_COLUMNS) - len(known)
