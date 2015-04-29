using UnityEngine;
using System.Collections;

public class Bush : MonoBehaviour {

	public Animator animator;

	public bool mouseIn = false;

	// Use this for initialization
	void Start () {
		//animator = gameObject.GetComponent<Animator>();

	}
	
	// Update is called once per frame
	void Update () {

	}

	void OnTriggerEnter(Collider other) {
		if(Random.value < 0.5){
			other.GetComponent<Mouse>().StopInBush();
		}
		animator.SetBool("MouseInside", true);
		mouseIn = true;
	}

	void OnTriggerExit(Collider other){
		animator.SetBool("MouseInside", false);
		mouseIn = false;
	}

}
