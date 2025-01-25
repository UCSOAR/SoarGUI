import { writable, type Writable } from 'svelte/store';

export const currentState = writable('N/A');
export const auth = writable(false);

export interface Stores {
	new_hybrid_ac2_open: Writable<any>;
	new_hybrid_pbv1_open: Writable<any>;
    new_hybrid_pbv2_open: Writable<any>;
    new_hybrid_pbv3_open: Writable<any>;
    new_hybrid_pbv4_open: Writable<any>;
    new_hybrid_pbv5_open: Writable<any>;
    new_hybrid_pbv6_open: Writable<any>;
	new_hybrid_sol5_open: Writable<any>;
    new_hybrid_sol6_open: Writable<any>
    new_hybrid_sol7_open: Writable<any>;
    new_hybrid_sol8a_open: Writable<any>;
    new_hybrid_sol8b_open: Writable<any>;
	new_hybrid_rcu_tc1_temperature: Writable<any>;
    new_hybrid_rcu_tc2_temperature: Writable<any>;
    new_hybrid_rcu_tc3_temperature: Writable<any>;
    new_hybrid_rcu_tc4_temperature: Writable<any>;
    new_hybrid_rcu_tc5_temperature: Writable<any>;
	new_hybrid_nos1_mass: Writable<any>;
	new_hybrid_nos2_mass: Writable<any>;
	new_hybrid_pt1_pressure: Writable<string | number | undefined>;
	new_hybrid_pt2_pressure: Writable<string | number | undefined>;
	new_hybrid_pt3_pressure: Writable<string | number | undefined>;
	new_hybrid_pt4_pressure: Writable<string | number | undefined>;
    new_hybrid_pt5_pressure: Writable<string | number | undefined>;
	system_state: Writable<string | undefined>;
	timer_state: Writable<string | undefined>;
	timer_period: Writable<number | undefined>;
	timer_remaining: Writable<number | undefined>;
	box1_on: Writable<any>;
	box2_on: Writable<any>;
}

export const initStores = () => {
	return {

		new_hybrid_ac2_open: writable(undefined),
		new_hybrid_pbv1_open: writable(undefined),
		new_hybrid_pbv2_open: writable(undefined),
		new_hybrid_pbv3_open: writable(undefined),
		new_hybrid_pbv4_open: writable(undefined),
		new_hybrid_pbv5_open: writable(undefined),
		new_hybrid_pbv6_open: writable(undefined),
		new_hybrid_sol5_open: writable(undefined),
		new_hybrid_sol6_open: writable(undefined),
		new_hybrid_sol7_open: writable(undefined),
		new_hybrid_sol8a_open: writable(undefined),
		new_hybrid_sol8b_open: writable(undefined),
		new_hybrid_rcu_tc1_temperature: writable(undefined),
		new_hybrid_rcu_tc2_temperature: writable(undefined),
		new_hybrid_rcu_tc3_temperature: writable(undefined),
		new_hybrid_rcu_tc4_temperature: writable(undefined),
		new_hybrid_rcu_tc5_temperature: writable(undefined),
		new_hybrid_nos1_mass: writable(undefined),
		new_hybrid_nos2_mass: writable(undefined),
		new_hybrid_pt1_pressure: writable<string | number | undefined>(undefined),
		new_hybrid_pt2_pressure: writable<string | number | undefined>(undefined),
		new_hybrid_pt3_pressure: writable<string | number | undefined>(undefined),
		new_hybrid_pt4_pressure: writable<string | number | undefined>(undefined),
		new_hybrid_pt5_pressure: writable<string | number | undefined>(undefined),
		system_state: writable<string | undefined>(undefined),
		timer_state: writable<string | undefined>(undefined),
		timer_period: writable<number | undefined>(undefined),
		timer_remaining: writable<number | undefined>(undefined),
		box1_on: writable(undefined),
		box2_on: writable(undefined),
	};
};
