from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
import os

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
topic = "Trending topics on social media with a potential to go viral"



@CrewBase
class LatestAiDevelopment():
	"""LatestAiDevelopment crew"""
	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			verbose=True
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the LatestAiDevelopment crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge
		search_tool = SerperDevTool(api_key=os.getenv("SERPER_API_KEY"))
		web_scraper = ScrapeWebsiteTool()

		researcher = Agent(
			role="Senior Data Researcher",
			goal="Find trending topics with viral potential from the most current sources",
			backstory="Expert at identifying emerging trends across platforms using real-time data",
			verbose=True,
			tools=[search_tool, web_scraper],
			allow_delegation=False
		)
		research_task = Task(
			description="""
			Conduct a thorough research about trending topics on social media with viral potential. 
			IMPORTANT:
			1. ONLY search for and report on content from {current_date} or more recent
			2. Explicitly verify and state the publication date of each source
			3. Reject any information that isn't from the current day
			4. Use web search tools to get the most up-to-date information
			5. Your report MUST include the current date ({current_date}) in the heading
			""",
			expected_output="A detailed report of trending topics from today with verified dates",
			agent=researcher
		)

		
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
