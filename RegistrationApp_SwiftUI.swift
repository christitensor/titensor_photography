import SwiftUI
import UIKit
import CoreImage.CIFilterBuiltins

// MARK: - Data Models

struct RegistrationEntry: Identifiable, Codable, Hashable {
    let id: UUID
    var controlNumber: Int
    var firstName: String
    var lastName: String
    var jerseyNumber: String
    var grade: String
    var school: String
    var sport: String
    var team: String
    var parentFirstName: String
    var parentLastName: String
    var parentPhone: String
    var parentEmail: String
    var eightByTen: String
    var teamPhoto: String
    var silverPackage: String
    var digitalCopy: String
    var banner: String
    var flex: String
    var frame: String
    var paymentType: String
    var paymentAmount: String
    var notes: String
    var qrImageData: Data?

    init(controlNumber: Int,
         firstName: String = "",
         lastName: String = "",
         jerseyNumber: String = "",
         grade: String = "9",
         school: String = "Ridgeline",
         sport: String = "Football",
         team: String = "Varsity",
         parentFirstName: String = "",
         parentLastName: String = "",
         parentPhone: String = "",
         parentEmail: String = "",
         eightByTen: String = "0",
         teamPhoto: String = "0",
         silverPackage: String = "0",
         digitalCopy: String = "0",
         banner: String = "0",
         flex: String = "0",
         frame: String = "0",
         paymentType: String = "Did not pay",
         paymentAmount: String = "0",
         notes: String = "") {
        self.id = UUID()
        self.controlNumber = controlNumber
        self.firstName = firstName
        self.lastName = lastName
        self.jerseyNumber = jerseyNumber
        self.grade = grade
        self.school = school
        self.sport = sport
        self.team = team
        self.parentFirstName = parentFirstName
        self.parentLastName = parentLastName
        self.parentPhone = parentPhone
        self.parentEmail = parentEmail
        self.eightByTen = eightByTen
        self.teamPhoto = teamPhoto
        self.silverPackage = silverPackage
        self.digitalCopy = digitalCopy
        self.banner = banner
        self.flex = flex
        self.frame = frame
        self.paymentType = paymentType
        self.paymentAmount = paymentAmount
        self.notes = notes
    }
}

final class SessionData: ObservableObject {
    @Published var entries: [RegistrationEntry] = []
    @Published var nextControlNumber: Int = 1

    private var documentsURL: URL {
        FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
    }

    private var sessionFileURL: URL {
        documentsURL.appendingPathComponent("session.json")
    }

    func loadSession() {
        do {
            let data = try Data(contentsOf: sessionFileURL)
            entries = try JSONDecoder().decode([RegistrationEntry].self, from: data)
            nextControlNumber = (entries.map { $0.controlNumber }.max() ?? 0) + 1
        } catch {
            print("Failed to load session: \(error)")
        }
    }

    func saveSession() {
        do {
            let data = try JSONEncoder().encode(entries)
            try data.write(to: sessionFileURL)
        } catch {
            print("Failed to save session: \(error)")
        }
    }

    func add(_ newEntry: RegistrationEntry) {
        entries.append(newEntry)
        nextControlNumber = (entries.map { $0.controlNumber }.max() ?? 0) + 1
        saveSession()
    }

    func update(_ updatedEntry: RegistrationEntry) {
        if let idx = entries.firstIndex(where: { $0.id == updatedEntry.id }) {
            entries[idx] = updatedEntry
            saveSession()
        }
    }

    func exportCSV(for sortedEntries: [RegistrationEntry]? = nil) -> URL? {
        let items = sortedEntries ?? entries
        var csv = "Control,First,Last,Jersey,Grade,School,Sport,Team,ParentFirst,ParentLast,ParentPhone,ParentEmail,8x10,TeamPhoto,Silver,Digital,Banner,Flex,Frame,PaymentType,PaymentAmount,Notes\n"
        for e in items {
            let row = [
                "\(e.controlNumber)", e.firstName, e.lastName, e.jerseyNumber, e.grade,
                e.school, e.sport, e.team, e.parentFirstName, e.parentLastName,
                e.parentPhone, e.parentEmail, e.eightByTen, e.teamPhoto,
                e.silverPackage, e.digitalCopy, e.banner, e.flex, e.frame,
                e.paymentType, e.paymentAmount,
                e.notes.replacingOccurrences(of: ",", with: ";")
            ]
            csv.append(row.joined(separator: ",") + "\n")
        }
        let url = FileManager.default.temporaryDirectory.appendingPathComponent("registration.csv")
        do {
            try csv.write(to: url, atomically: true, encoding: .utf8)
            return url
        } catch {
            print("CSV export failed: \(error)")
            return nil
        }
    }

    func printRosterByNumber() -> URL? {
        let sorted = entries.sorted { $0.jerseyNumber < $1.jerseyNumber }
        return exportCSV(for: sorted)
    }

    func printRosterByGrade() -> URL? {
        let sorted = entries.sorted { $0.grade < $1.grade }
        return exportCSV(for: sorted)
    }
}

// MARK: - Helpers

func generateQRCode(from string: String) -> UIImage? {
    let filter = CIFilter.qrCodeGenerator()
    let data = Data(string.utf8)
    filter.setValue(data, forKey: "inputMessage")
    filter.setValue("Q", forKey: "inputCorrectionLevel")
    if let outputImage = filter.outputImage {
        let scaled = outputImage.transformed(by: CGAffineTransform(scaleX: 10, y: 10))
        return UIImage(ciImage: scaled)
    }
    return nil
}

struct ShareSheet: UIViewControllerRepresentable {
    let activityItems: [Any]
    func makeUIViewController(context: Context) -> UIActivityViewController {
        UIActivityViewController(activityItems: activityItems, applicationActivities: nil)
    }
    func updateUIViewController(_ uiViewController: UIActivityViewController, context: Context) {}
}

// MARK: - App

@main
struct TitensorRegistrationApp: App {
    @StateObject private var sessionData = SessionData()
    var body: some Scene {
        WindowGroup {
            NavigationSplitView {
                SidebarView()
                    .environmentObject(sessionData)
            } detail: {
                RegistrationFormView()
                    .environmentObject(sessionData)
            }
        }
    }
}

enum SidebarSelection: Hashable {
    case register, sessionData, exportData
}

struct SidebarView: View {
    @EnvironmentObject var sessionData: SessionData
    var body: some View {
        List {
            NavigationLink(value: SidebarSelection.register) {
                Label("New Registration", systemImage: "person.badge.plus")
            }
            NavigationLink(value: SidebarSelection.sessionData) {
                Label("Session Data", systemImage: "list.bullet.rectangle")
            }
            NavigationLink(value: SidebarSelection.exportData) {
                Label("Export Data", systemImage: "square.and.arrow.up")
            }
        }
        .listStyle(.sidebar)
        .navigationTitle("Titensor")
        .navigationDestination(for: SidebarSelection.self) { sel in
            switch sel {
            case .register:
                RegistrationFormView().environmentObject(sessionData)
            case .sessionData:
                SessionListView().environmentObject(sessionData)
            case .exportData:
                ExportView().environmentObject(sessionData)
            }
        }
    }
}

// MARK: - Registration Form

struct RegistrationFormView: View {
    @EnvironmentObject var sessionData: SessionData

    @State private var entry = RegistrationEntry(controlNumber: 1)
    @State private var qrImage: UIImage?
    @State private var showShare = false
    @State private var shareURL: URL?

    let grades = ["9","10","11","12","Coach"]
    let schools = ["Ridgeline","Preston","Green Canyon","Skyview","Logan","N/A"]
    let sports = ["Football","Tennis","Soccer","Volleyball","Cross Country","Golf","Cheer"]
    let teams = ["Varsity","JV","Freshman","N/A"]
    let paymentTypes = ["Cash","Card","Check","Did not pay"]

    var body: some View {
        Form {
            Section(header: Text("Session")) {
                HStack {
                    Button("Resume Session") { sessionData.loadSession() }
                    Spacer()
                    Button("Upload Teams") { /* implement Excel import */ }
                }
            }
            Section(header: Text("Athlete Info")) {
                TextField("First Name", text: $entry.firstName)
                TextField("Last Name", text: $entry.lastName)
                TextField("Jersey #", text: $entry.jerseyNumber)
                Picker("Grade", selection: $entry.grade) {
                    ForEach(grades, id: \..self) { Text($0) }
                }
                Picker("School", selection: $entry.school) {
                    ForEach(schools, id: \..self) { Text($0) }
                }
                Picker("Sport", selection: $entry.sport) {
                    ForEach(sports, id: \..self) { Text($0) }
                }
                Picker("Team", selection: $entry.team) {
                    ForEach(teams, id: \..self) { Text($0) }
                }
            }
            Section(header: Text("Parent / Guardian")) {
                TextField("Parent First", text: $entry.parentFirstName)
                TextField("Parent Last", text: $entry.parentLastName)
                TextField("Phone", text: $entry.parentPhone)
                TextField("Email", text: $entry.parentEmail)
            }
            Section(header: Text("Package Quantities")) {
                TextField("8×10", text: $entry.eightByTen)
                TextField("Team Photo", text: $entry.teamPhoto)
                TextField("Silver", text: $entry.silverPackage)
                TextField("Digital", text: $entry.digitalCopy)
                TextField("Banner", text: $entry.banner)
                TextField("Flex", text: $entry.flex)
                TextField("Frame", text: $entry.frame)
            }
            Section(header: Text("Payment")) {
                Picker("Type", selection: $entry.paymentType) {
                    ForEach(paymentTypes, id: \..self) { Text($0) }
                }
                TextField("Amount", text: $entry.paymentAmount)
                    .keyboardType(.decimalPad)
            }
            Section(header: Text("Notes")) {
                TextEditor(text: $entry.notes)
                    .frame(height: 100)
            }
            if let img = qrImage {
                Section(header: Text("QR")) {
                    Image(uiImage: img).resizable().interpolation(.none)
                        .scaledToFit().frame(width:200,height:200)
                }
            }
            Button("Generate") {
                entry.controlNumber = sessionData.nextControlNumber
                if let qr = generateQRCode(from: "\(entry.controlNumber)") {
                    qrImage = qr
                    entry.qrImageData = qr.pngData()
                }
                sessionData.add(entry)
                entry = RegistrationEntry(controlNumber: sessionData.nextControlNumber)
            }
        }
        .navigationTitle("New Registration")
        .sheet(isPresented: $showShare) {
            if let url = shareURL { ShareSheet(activityItems: [url]) }
        }
    }
}

// MARK: - Session List View

struct SessionListView: View {
    @EnvironmentObject var sessionData: SessionData
    var body: some View {
        List(sessionData.entries) { entry in
            NavigationLink(value: entry) {
                VStack(alignment: .leading) {
                    Text("#\(entry.controlNumber) - \(entry.firstName) \(entry.lastName)")
                    Text("Jersey \(entry.jerseyNumber) - \(entry.sport)")
                        .font(.caption).foregroundColor(.secondary)
                }
            }
        }
        .navigationDestination(for: RegistrationEntry.self) { e in
            EditDetailView(entry: e).environmentObject(sessionData)
        }
        .navigationTitle("Session Data")
    }
}

// MARK: - Edit View

struct EditDetailView: View {
    @EnvironmentObject var sessionData: SessionData
    @State var entry: RegistrationEntry
    @State private var qrImage: UIImage?

    let grades = ["9","10","11","12","Coach"]
    let schools = ["Ridgeline","Preston","Green Canyon","Skyview","Logan","N/A"]
    let sports = ["Football","Tennis","Soccer","Volleyball","Cross Country","Golf","Cheer"]
    let teams = ["Varsity","JV","Freshman","N/A"]
    let paymentTypes = ["Cash","Card","Check","Did not pay"]

    var body: some View {
        Form {
            Section(header: Text("Athlete Info")) {
                TextField("First Name", text: $entry.firstName)
                TextField("Last Name", text: $entry.lastName)
                TextField("Jersey #", text: $entry.jerseyNumber)
                Picker("Grade", selection: $entry.grade) { ForEach(grades,id: \..self){Text($0)} }
                Picker("School", selection: $entry.school) { ForEach(schools,id: \..self){Text($0)} }
                Picker("Sport", selection: $entry.sport) { ForEach(sports,id: \..self){Text($0)} }
                Picker("Team", selection: $entry.team) { ForEach(teams,id: \..self){Text($0)} }
            }
            Section(header: Text("Parent / Guardian")) {
                TextField("Parent First", text: $entry.parentFirstName)
                TextField("Parent Last", text: $entry.parentLastName)
                TextField("Phone", text: $entry.parentPhone)
                TextField("Email", text: $entry.parentEmail)
            }
            Section(header: Text("Packages")) {
                TextField("8×10", text: $entry.eightByTen)
                TextField("Team Photo", text: $entry.teamPhoto)
                TextField("Silver", text: $entry.silverPackage)
                TextField("Digital", text: $entry.digitalCopy)
                TextField("Banner", text: $entry.banner)
                TextField("Flex", text: $entry.flex)
                TextField("Frame", text: $entry.frame)
            }
            Section(header: Text("Payment")) {
                Picker("Type", selection: $entry.paymentType) { ForEach(paymentTypes,id: \..self){Text($0)} }
                TextField("Amount", text: $entry.paymentAmount)
            }
            Section(header: Text("Notes")) {
                TextEditor(text: $entry.notes).frame(height:100)
            }
            if let img = qrImage ?? entry.qrImageData.flatMap(UIImage.init(data:)) {
                Section(header: Text("QR")) {
                    Image(uiImage: img).resizable().interpolation(.none)
                        .scaledToFit().frame(width:200,height:200)
                }
            }
            Button("Save Changes") {
                if let qr = generateQRCode(from: "\(entry.controlNumber)") {
                    qrImage = qr
                    entry.qrImageData = qr.pngData()
                }
                sessionData.update(entry)
            }
        }
        .navigationTitle("Edit Entry")
    }
}

// MARK: - Export View

struct ExportView: View {
    @EnvironmentObject var sessionData: SessionData
    @State private var showShare = false
    @State private var shareURL: URL?
    var body: some View {
        VStack(spacing: 24) {
            Button("Export to CSV") {
                shareURL = sessionData.exportCSV()
                showShare = shareURL != nil
            }
            Button("Print Roster by Number") {
                shareURL = sessionData.printRosterByNumber()
                showShare = shareURL != nil
            }
            Button("Print Roster by Grade") {
                shareURL = sessionData.printRosterByGrade()
                showShare = shareURL != nil
            }
        }
        .frame(maxWidth: .infinity)
        .navigationTitle("Export Data")
        .sheet(isPresented: $showShare) {
            if let url = shareURL { ShareSheet(activityItems: [url]) }
        }
    }
}


