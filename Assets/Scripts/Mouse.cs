﻿using UnityEngine;
using System.Collections;

public class Mouse : MonoBehaviour {

	public float leftLimit = -6.0f;
	public float rightLimit = 6.0f;
	public float speed = 2.0f;

	public bool isGoingLeft = true;
	public bool isStopped = false;
	public bool isTurning = false;
	public string direction;
	float rotationDamping = 5.0f;
	private Quaternion targetRotation;
	private Vector3 tempPosition;

	// Use this for initialization
	void Start () {
	
	}
	
	// Update is called once per frame
	void Update () {

		MovementAI ();
	
	}

	void Spawn(){

	}

	void Despawn(){

	}

	void Jump(){

	}

	void MovementAI(){


		if(isTurning){
			Rotate180 ();
		}

		else if(isGoingLeft){
			direction = "left";
			MoveLeft ();
		}
		else {
			direction = "right";
			MoveRight ();
		}


		if (gameObject.transform.position.x < leftLimit){
			isGoingLeft = false;
			isTurning = true;
			tempPosition = new Vector3(leftLimit, gameObject.transform.position.y, gameObject.transform.position.z);
			gameObject.transform.position = tempPosition;
		}

		if (gameObject.transform.position.x > rightLimit){
			isGoingLeft = true;
			isTurning = true;
			tempPosition = new Vector3(rightLimit, gameObject.transform.position.y, gameObject.transform.position.z);
			gameObject.transform.position = tempPosition;
		}

	}

	void MoveRight(){
		gameObject.transform.Translate(Vector3.right * Time.deltaTime * speed, Space.World);
	}

	void MoveLeft(){
		gameObject.transform.Translate(Vector3.left * Time.deltaTime * speed, Space.World);
	}

	void Rotate180() {
		if (isGoingLeft){
			targetRotation = Quaternion.Euler(0f, 360f, 0f);

		}
		else {
			targetRotation = Quaternion.Euler(0f, 180f, 0f);

		}

		gameObject.transform.rotation = Quaternion.Slerp(gameObject.transform.rotation, targetRotation, Time.deltaTime * rotationDamping);

		if ( Mathf.Abs(gameObject.transform.eulerAngles.y - targetRotation.eulerAngles.y) < 1f ) {
			targetRotation.eulerAngles = new Vector3(0f, Mathf.RoundToInt(targetRotation.eulerAngles.y), 0f);
			gameObject.transform.rotation = targetRotation;
			isTurning = false;

		}

	}

}