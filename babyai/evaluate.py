# Returns the performance of the agent on the environment for a particular number of episodes.
def evaluate(agent, env, episodes):
    # Initialize logs
    logs = {"num_frames_per_episode": [], "return_per_episode": [], "observations_per_episode": []}

    for _ in range(episodes):
        obs = env.reset()
        done = False

        num_frames = 0
        returnn = 0
        obss = []
        while not(done):
            action = agent.get_action(obs)
            obss.append(obs)
            obs, reward, done, _ = env.step(action)
            agent.analyze_feedback(reward, done)
            num_frames += 1
            returnn += reward

        logs["observations_per_episode"].append(obss)
        logs["num_frames_per_episode"].append(num_frames)
        logs["return_per_episode"].append(returnn)

    return logs