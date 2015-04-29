using UnityEngine;
using System.Collections;

[ExecuteInEditMode]
public class Sapin: MonoBehaviour {

	public float scale;
	public float scaleMin;
	public float scaleMax;
	public float distanceFactor;
	public float distance;
	public GameObject camera;


	void Start() {
		camera = GameObject.Find("Main Camera");
		distance = camera.transform.position.z - gameObject.transform.position.z;
		scale = Random.Range(scaleMin, scaleMax) * distanceFactor / distance;
		gameObject.transform.localScale = new Vector3(scale, scale, scale);
	
	}

}
