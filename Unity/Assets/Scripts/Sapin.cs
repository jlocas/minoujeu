using UnityEngine;
using System.Collections;

public class Sapin: MonoBehaviour {

	public float scale;
	public float scaleMin;
	public float scaleMax;
	public float distanceFactor;
	public float distance;
	public GameObject camera;

	// Use this for initialization
	void Start () {
		camera = GameObject.Find("Main Camera");
		distance = camera.transform.position.z - gameObject.transform.position.z;
		scale = Random.Range(scaleMin, scaleMax) * distanceFactor / distance;
		gameObject.transform.localScale = new Vector3(scale, scale, scale);
	
	}
	
	// Update is called once per frame
	void Update () {
	
	}
}
