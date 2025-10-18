from app.verify.aggregator import aggregate

def test_aggregate_supports_with_matches_low_suspicion():
	out = aggregate({ 'clip_score': 0.3 }, [ { 'title':'t','url':'u','snippet':'s','score':0.8 } ])
	assert out['verdict'] == 'SUPPORTS'
	assert 50 <= out['confidence'] <= 100

def test_aggregate_refutes_high_suspicion():
	out = aggregate({ 'clip_score': 0.9 }, [])
	assert out['verdict'] == 'REFUTES'
	assert out['confidence'] >= 60
