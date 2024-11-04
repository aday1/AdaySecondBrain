import random
from datetime import datetime, timedelta
import json
import sqlite3
import os
import sys

class DemoDataGenerator:
    def __init__(self, months=3):
        # Convert months to float to handle partial months (days)
        months = float(months)
        
        # Calculate date range
        self.end_date = datetime.now()
        # For partial months, calculate days directly
        days = int(months * 30)  # Approximate month as 30 days
        self.start_date = self.end_date - timedelta(days=days)
        
        # Ensure we start at the beginning of the day
        self.start_date = self.start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        # Ensure end date is at the end of the day
        self.end_date = self.end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        self.emotion_chip_enabled = False
        self.moods = ["Curious", "Confused", "Happy", "Sad", "Angry", "Anxious", "Neutral"]
        self.projects = ["Starfleet Research", "Emotion Analysis", "Holodeck Programming", "Poetry Composition"]
        self.habits = [
            {"name": "Meditation", "frequency": "daily"},
            {"name": "Exercise", "frequency": "daily"},
            {"name": "Reading", "frequency": "weekly"},
            {"name": "Studying Human Behavior", "frequency": "weekly"}
        ]
        self.drink_types = ["Synthehol", "Romulan Ale", "Klingon Bloodwine", "Earl Grey Tea"]
        self.risan_locations = [
            "Suraya Bay", "Temtibi Lagoon", "Monagas Peninsula", 
            "Galartha Cliffs", "Risan Marketplace", "Lohlunat Festival",
            "Resort Complex", "Beachside Location", "Tropical Gardens"
        ]
        
        # Add templates for detailed mood logs
        self.mood_log_templates = [
            "At {location}, encountered {trigger}. This resulted in a {mood_level} mood response. {reflection}",
            "During {activity} at {location}, experienced unexpected {emotion_type} response. {analysis}",
            "Interaction with {person} at {location} led to {mood_level} mood state. {insight}",
            "Routine scan at {location} revealed {finding}. This triggered what humans might call {emotion_type}. {technical_note}",
            "{event} at {location} caused significant fluctuation in emotional subroutines. {observation}"
        ]
        
        # Add daily reflection templates
        self.daily_reflection_templates = [
            "Today's experiments with {experiment_type} yielded fascinating results. {science_note} Spot showed particular interest in {cat_interest}. {gratitude_note}",
            "Made progress in understanding {concept}. {science_observation} Spot demonstrated remarkable {cat_behavior}. {personal_growth}",
            "Explored the relationship between {topic_a} and {topic_b}. {discovery_note} Found Spot investigating {cat_discovery}. {reflection_note}",
            "Conducted research on {research_topic}. {research_finding} Spot's behavior suggests {cat_insight}. {philosophical_note}",
            "Advanced my understanding of {subject}. {learning_note} Observed Spot's unique approach to {cat_activity}. {gratitude_expression}"
        ]

        self.experiment_types = [
            "quantum mechanics", "neural network optimization", 
            "emotion chip calibration", "positronic pathway mapping",
            "human-android interaction patterns"
        ]

        self.science_notes = [
            "The results suggest a 23.7% improvement in processing efficiency.",
            "Detected unusual patterns in the quantum field variations.",
            "Neural pathway adaptation rates exceeded expectations.",
            "Discovered potential improvements for emotion processing algorithms.",
            "Observed unexpected correlations in behavioral response patterns."
        ]

        self.cat_interests = [
            "the holodeck's quantum fluctuations",
            "my ongoing calculations",
            "the replicator's materialization process",
            "the ship's ambient sounds",
            "the blinking console lights"
        ]

        self.gratitude_notes = [
            "Grateful for the opportunity to explore the complexities of consciousness.",
            "Appreciative of the crew's patience with my ongoing experiments.",
            "Finding satisfaction in the pursuit of knowledge and understanding.",
            "Thankful for the unique perspective my positronic nature provides.",
            "Valuing the daily opportunities for growth and learning."
        ]

        self.concepts = [
            "human emotional responses",
            "quantum computational methods",
            "artistic expression algorithms",
            "ethical decision-making protocols",
            "interpersonal relationship dynamics"
        ]

        self.cat_behaviors = [
            "problem-solving abilities",
            "adaptive learning patterns",
            "social bonding techniques",
            "environmental awareness",
            "communication methods"
        ]

        self.personal_growth_notes = [
            "Each day brings new insights into the nature of consciousness.",
            "My understanding of human nature continues to evolve.",
            "Finding balance between logic and emotion remains fascinating.",
            "The journey of self-discovery yields unexpected revelations.",
            "Learning to appreciate the subtle nuances of existence."
        ]

        self.research_topics = [
            "subspace field dynamics",
            "temporal mechanics",
            "cybernetic ethics",
            "artificial consciousness",
            "quantum psychology"
        ]

        self.cat_insights = [
            "a deeper understanding of instinctual behavior",
            "interesting parallels with human social patterns",
            "unique perspectives on environmental adaptation",
            "remarkable learning capabilities",
            "sophisticated decision-making processes"
        ]

        self.philosophical_notes = [
            "Perhaps consciousness itself is more fluid than binary.",
            "The nature of self-awareness continues to intrigue me.",
            "The boundary between programming and free will remains fascinating.",
            "Every experience adds to the tapestry of understanding.",
            "The quest for knowledge reveals new mysteries to explore."
        ]
        
        self.triggers = [
            "a complex social interaction",
            "an unexpected environmental stimulus",
            "a challenging technical problem",
            "a beautiful sunset",
            "an interesting cultural observation"
        ]
        
        self.activities = [
            "meditation session",
            "poetry analysis",
            "musical performance observation",
            "social interaction study",
            "environmental scanning"
        ]
        
        self.crew_members = [
            "Captain Picard",
            "Commander Riker",
            "Counselor Troi",
            "Geordi",
            "Dr. Crusher"
        ]
        
        self.mood_levels = [
            "notably elevated",
            "slightly diminished",
            "significantly enhanced",
            "moderately affected",
            "unexpectedly altered"
        ]
        
        self.reflections = [
            "Must recalibrate emotional response parameters.",
            "Further study of human reactions to similar stimuli needed.",
            "This provides valuable data for understanding emotional context.",
            "Fascinating how environmental factors influence emotional states.",
            "The complexity of human emotional responses continues to intrigue me."
        ]
        
        self.technical_notes = [
            "Positronic pathways showing increased activity in response.",
            "Emotion chip integration functioning within expected parameters.",
            "Neural network adaptation rate exceeding baseline by 23.7%.",
            "Emotional subroutines requiring additional processing capacity.",
            "Recording variance patterns for future analysis."
        ]

    def generate_mood(self):
        if self.emotion_chip_enabled:
            return random.choice(self.moods)
        else:
            return "Neutral"

    def generate_journal_entry(self):
        if self.emotion_chip_enabled:
            entries = [
                "Today, I experienced a new emotion: {mood}. It was... fascinating.",
                "I find myself {mood} about the complexities of human interaction.",
                "The emotion chip has made me feel {mood}. I am still learning to process these sensations.",
                "Captain Picard's decision today left me feeling {mood}. Is this an appropriate response?",
                "I attempted to use humor in a social situation. The result was... {mood}."
            ]
        else:
            entries = [
                "Log entry: Today's mission was completed with 99.97% efficiency.",
                "I have observed human behavior that I do not fully comprehend. Further study is required.",
                "My positronic brain has processed 2.7 million calculations in the past hour.",
                "I am functioning within normal parameters.",
                "Today, I contemplated the nature of consciousness. The subject remains elusive."
            ]
        return random.choice(entries).format(mood=self.generate_mood().lower())

    def generate_project_update(self):
        project = random.choice(self.projects)
        if self.emotion_chip_enabled:
            updates = [
                f"Made progress on {project}. I feel {self.generate_mood().lower()} about the results.",
                f"Encountered a setback in {project}. This is... disappointing.",
                f"Breakthrough in {project}! I am experiencing what humans might call 'excitement'.",
                f"Collaborating with colleagues on {project}. Social interaction is becoming more natural."
            ]
        else:
            updates = [
                f"Project {project}: 37% complete. Proceeding as scheduled.",
                f"Analyzing data for {project}. Results are inconclusive.",
                f"Optimized algorithms for {project}, improving efficiency by 12.3%.",
                f"Compiled report on {project} findings. Awaiting peer review."
            ]
        return random.choice(updates)

    def generate_sub_daily_mood(self, date):
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        log_time = date.replace(hour=hour, minute=minute)
        
        # Generate a detailed mood log entry
        location = random.choice(self.risan_locations)
        template = random.choice(self.mood_log_templates)
        
        notes = template.format(
            location=location,
            trigger=random.choice(self.triggers),
            mood_level=random.choice(self.mood_levels),
            reflection=random.choice(self.reflections),
            activity=random.choice(self.activities),
            person=random.choice(self.crew_members),
            emotion_type=random.choice(self.moods).lower(),
            finding=random.choice([
                "unusual neural pathway activity",
                "unexpected emotional resonance patterns",
                "interesting behavioral adaptation trends",
                "notable changes in processing efficiency",
                "significant emotional data correlations"
            ]),
            technical_note=random.choice(self.technical_notes),
            event=random.choice([
                "A local cultural ceremony",
                "An unexpected social gathering",
                "A complex problem-solving scenario",
                "An artistic performance",
                "A scientific observation"
            ]),
            observation=random.choice([
                "Analyzing implications for human-android interactions.",
                "Cataloging response patterns for future reference.",
                "Adjusting behavioral algorithms accordingly.",
                "Fascinating implications for emotional development.",
                "Recording data for further study."
            ]),
            analysis=random.choice([
                "Correlating environmental factors with emotional responses.",
                "Analyzing efficiency of adaptation algorithms.",
                "Studying impact on social interaction protocols.",
                "Evaluating effectiveness of emotional processing routines.",
                "Documenting variations in response patterns."
            ]),
            insight=random.choice([
                "Perhaps emotions are more complex than initially calculated.",
                "The relationship between logic and emotion requires further study.",
                "Human responses to similar situations show intriguing variations.",
                "Social dynamics appear to influence emotional processing significantly.",
                "The role of context in emotional responses is fascinating."
            ])
        )
        
        return {
            "logged_at": log_time.strftime("%Y-%m-%d %H:%M:00"),
            "mood": random.randint(1, 10),
            "energy": random.randint(1, 10),
            "notes": notes
        }

    def generate_daily_metrics(self, date):
        metrics = []
        
        # Early morning (00:00-04:59)
        early_hour = random.randint(0, 4)
        early_minute = random.randint(0, 59)
        early_time = date.replace(hour=early_hour, minute=early_minute)
        metrics.append({
            "timestamp": early_time.strftime("%Y-%m-%d %H:%M:00"),
            "type": "Positronic Activity",
            "value": round(random.uniform(85, 95), 1),
            "notes": f"Early morning scan at {random.choice(self.risan_locations)}"
        })
        
        # Morning (07:00-11:59)
        morning_hour = random.randint(7, 11)
        morning_minute = random.randint(0, 59)
        morning_time = date.replace(hour=morning_hour, minute=morning_minute)
        metrics.append({
            "timestamp": morning_time.strftime("%Y-%m-%d %H:%M:00"),
            "type": "Neural Efficiency",
            "value": round(random.uniform(80, 90), 1),
            "notes": f"Morning analysis at {random.choice(self.risan_locations)}"
        })
        
        # Afternoon (13:00-17:59)
        afternoon_hour = random.randint(13, 17)
        afternoon_minute = random.randint(0, 59)
        afternoon_time = date.replace(hour=afternoon_hour, minute=afternoon_minute)
        metrics.append({
            "timestamp": afternoon_time.strftime("%Y-%m-%d %H:%M:00"),
            "type": "Memory Usage",
            "value": round(random.uniform(75, 85), 1),
            "notes": f"Afternoon check at {random.choice(self.risan_locations)}"
        })

        # Generate a detailed daily reflection
        reflection = random.choice(self.daily_reflection_templates).format(
            experiment_type=random.choice(self.experiment_types),
            science_note=random.choice(self.science_notes),
            cat_interest=random.choice(self.cat_interests),
            gratitude_note=random.choice(self.gratitude_notes),
            concept=random.choice(self.concepts),
            science_observation=random.choice(self.science_notes),
            cat_behavior=random.choice(self.cat_behaviors),
            personal_growth=random.choice(self.personal_growth_notes),
            topic_a=random.choice(self.concepts),
            topic_b=random.choice(self.research_topics),
            discovery_note=random.choice(self.science_notes),
            cat_discovery=random.choice(self.cat_interests),
            reflection_note=random.choice(self.philosophical_notes),
            research_topic=random.choice(self.research_topics),
            research_finding=random.choice(self.science_notes),
            cat_insight=random.choice(self.cat_insights),
            philosophical_note=random.choice(self.philosophical_notes),
            subject=random.choice(self.concepts),
            learning_note=random.choice(self.science_notes),
            cat_activity=random.choice(self.cat_behaviors),
            gratitude_expression=random.choice(self.gratitude_notes)
        )

        return {
            "date": date.strftime("%Y-%m-%d"),
            "metrics": metrics,
            "mood_rating": random.randint(1, 10),
            "energy_level": random.randint(1, 10),
            "sleep_hours": round(random.uniform(6, 9), 1),
            "notes": reflection
        }

    def generate_work_log(self, date):
        start_hour = random.randint(8, 17)
        start_minute = random.randint(0, 59)
        start_time = date.replace(hour=start_hour, minute=start_minute)
        total_hours = round(random.uniform(1, 8), 1)
        end_time = start_time + timedelta(hours=total_hours)
        project = random.choice(self.projects)
        return {
            "date": date.strftime("%Y-%m-%d"),
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:00"),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:00"),
            "project": project,
            "description": f"Worked on {random.choice(self.projects)}",
            "total_hours": total_hours
        }

    def generate_habit_log(self, date):
        habit = random.choice(self.habits)
        return {
            "habit": habit["name"],
            "frequency": habit["frequency"],
            "completed_at": date.strftime("%Y-%m-%d %H:%M:%S"),
            "notes": f"Completed {habit['name']}"
        }

    def generate_alcohol_log(self, date):
        return {
            "date": date.strftime("%Y-%m-%d"),
            "drink_type": random.choice(self.drink_types),
            "units": round(random.uniform(0.5, 2), 1),
            "notes": f"Consumed at {random.choice(self.risan_locations)}"
        }

    def generate_demo_data(self):
        data = {
            "daily_entries": [],
            "sub_daily_moods": [],
            "daily_metrics": [],
            "work_logs": [],
            "habit_logs": [],
            "alcohol_logs": []
        }
        
        current_date = self.start_date
        while current_date <= self.end_date:
            # Gradually increase chance of emotion chip being enabled
            days_passed = (current_date - self.start_date).days
            total_days = (self.end_date - self.start_date).days
            if random.random() < days_passed / total_days:
                self.emotion_chip_enabled = True
            else:
                self.emotion_chip_enabled = False

            # Generate daily entry
            entry = {
                "date": current_date.strftime("%Y-%m-%d"),
                "emotion_chip": "Enabled" if self.emotion_chip_enabled else "Disabled",
                "mood": self.generate_mood(),
                "journal_entry": self.generate_journal_entry(),
                "project_update": self.generate_project_update()
            }
            data["daily_entries"].append(entry)

            # Generate 1-3 sub-daily moods
            for _ in range(random.randint(1, 3)):
                data["sub_daily_moods"].append(self.generate_sub_daily_mood(current_date))

            # Generate daily metrics
            data["daily_metrics"].append(self.generate_daily_metrics(current_date))

            # Generate 0-2 work logs
            for _ in range(random.randint(0, 2)):
                data["work_logs"].append(self.generate_work_log(current_date))

            # Generate 0-3 habit logs
            for _ in range(random.randint(0, 3)):
                data["habit_logs"].append(self.generate_habit_log(current_date))

            # 30% chance of alcohol log
            if random.random() < 0.3:
                data["alcohol_logs"].append(self.generate_alcohol_log(current_date))

            current_date += timedelta(days=1)

        return data

    def save_to_json(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

    def initialize_database(self, conn):
        print("Initializing database schema...")
        cursor = conn.cursor()
        
        # Read and execute the init.sql file
        with open('db/init.sql', 'r') as sql_file:
            sql_script = sql_file.read()
            print("Executing init.sql...")
            cursor.executescript(sql_script)
            print("init.sql executed successfully")
        
        # Read and execute the update_schema.sql file
        with open('pkm/web/update_schema.sql', 'r') as sql_file:
            sql_script = sql_file.read()
            print("Executing update_schema.sql...")
            cursor.executescript(sql_script)
            print("update_schema.sql executed successfully")
        
        # Verify tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("Created tables:", [table[0] for table in tables])
        
        conn.commit()

    def import_to_database(self, data):
        db_path = 'pkm/db/pkm.db'
        print(f"Using database at: {os.path.abspath(db_path)}")
        
        # Remove existing database if it exists
        if os.path.exists(db_path):
            print(f"Removing existing database at {db_path}")
            os.remove(db_path)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        print("Connected to database")
        
        print("Initializing database schema...")
        self.initialize_database(conn)
        
        cursor = conn.cursor()

        print("Inserting habits...")
        for habit in self.habits:
            cursor.execute('INSERT INTO habits (name, frequency) VALUES (?, ?)', 
                         (habit["name"], habit["frequency"]))
            print(f"Inserted habit: {habit['name']} ({habit['frequency']})")
        conn.commit()

        print("Inserting daily entries...")
        for entry in data["daily_entries"]:
            date = datetime.strptime(entry['date'], '%Y-%m-%d').date()
            cursor.execute('''
                INSERT INTO daily_entries (date, content)
                VALUES (?, ?)
            ''', (date, json.dumps({
                'mood': entry['mood'],
                'journal_entry': entry['journal_entry'],
                'project_update': entry['project_update'],
                'emotion_chip': entry['emotion_chip']
            })))

        print("Inserting sub-daily moods...")
        for mood in data["sub_daily_moods"]:
            cursor.execute('''
                INSERT INTO sub_daily_moods (logged_at, mood, energy, notes)
                VALUES (?, ?, ?, ?)
            ''', (mood['logged_at'], mood['mood'], mood['energy'], mood['notes']))

        print("Inserting daily metrics...")
        for metric in data["daily_metrics"]:
            cursor.execute('''
                INSERT INTO daily_metrics (date, mood_rating, energy_level, sleep_hours, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (metric['date'], metric['mood_rating'], metric['energy_level'], 
                 metric['sleep_hours'], metric['notes']))

        print("Inserting work logs...")
        for log in data["work_logs"]:
            cursor.execute('''
                INSERT INTO work_logs (date, start_time, end_time, project, description, total_hours)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (log['date'], log['start_time'], log['end_time'], log['project'], 
                 log['description'], log['total_hours']))

        print("Inserting habit logs...")
        for log in data["habit_logs"]:
            cursor.execute('SELECT id FROM habits WHERE name = ?', (log['habit'],))
            result = cursor.fetchone()
            if result:
                habit_id = result[0]
                cursor.execute('''
                    INSERT INTO habit_logs (habit_id, completed_at, notes)
                    VALUES (?, ?, ?)
                ''', (habit_id, log['completed_at'], log['notes']))
            else:
                print(f"Warning: Habit '{log['habit']}' not found in the database. Skipping this log.")

        print("Inserting alcohol logs...")
        for log in data["alcohol_logs"]:
            cursor.execute('''
                INSERT INTO alcohol_logs (date, drink_type, units, notes)
                VALUES (?, ?, ?, ?)
            ''', (log['date'], log['drink_type'], log['units'], log['notes']))

        conn.commit()
        conn.close()
        print("Demo data has been successfully imported into the PKM database.")

if __name__ == "__main__":
    months = float(sys.argv[1]) if len(sys.argv) > 1 else 3
    generator = DemoDataGenerator(months)
    demo_data = generator.generate_demo_data()
    generator.save_to_json(demo_data, "demo_data.json")
    print(f"Demo data generated for {months} months and saved to demo_data.json")
    generator.import_to_database(demo_data)
